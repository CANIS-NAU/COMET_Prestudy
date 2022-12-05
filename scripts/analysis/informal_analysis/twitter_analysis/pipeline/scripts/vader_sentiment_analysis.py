# %%
# Run through each each cleaned post and run VADER Sentiment analysis 

# %%
import pandas as pd

# Temp file path
filepath = input()

# Load the data
twitter_data = pd.read_csv(filepath)

twitter_data.head()

# %% [markdown]
# # Run through vader, adding new column with sentiment data

# %%
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

twitter_data["sentiment"] = twitter_data.apply(lambda row: analyzer.polarity_scores(str(row["clntxt"])), axis=1)

twitter_data = pd.concat([twitter_data.drop("sentiment", axis=1), pd.json_normalize(twitter_data["sentiment"])], axis=1)

twitter_data


# %%
# convert all dates to datetime objects

def extract_ymd(time: str):
    str_build = ""
    for char in time:
        if char == 'T':
            return str_build
        else: str_build += char

# clean dates in table
import calendar
from numpy import int64

twitter_data["date"] = twitter_data["created_at"].apply(extract_ymd)
twitter_data["month"] = pd.DatetimeIndex(twitter_data['date']).month.fillna(0).astype(int64)
twitter_data['month'] = twitter_data['month'].apply(lambda x: calendar.month_abbr[x])
twitter_data["year"] = pd.DatetimeIndex(twitter_data['date']).year

twitter_data["standardized_compound"] = ((twitter_data['compound'] - twitter_data['compound'].mean()) / twitter_data['compound'].std())

twitter_data

# %%
import seaborn as sns
import matplotlib.pyplot as plt

tdata_neu = twitter_data[(twitter_data["compound"] == 0)].index
tdata_neu_normalized = twitter_data.drop(tdata_neu)
tdata_neu_counts = tdata_neu.size
tdata_tot_counts = twitter_data["id"].size
proportion_of_neutral = tdata_neu_counts/tdata_tot_counts

##### Other visualizations ######
#sns.swarmplot(data=twitter_data, x="5", y="compound", color="k", size=3, ax=g.ax)

# Proportion of neutral posts to total post counts
print("Proportion of neutral posts to total post counts: ", proportion_of_neutral, "\n", tdata_neu_counts, "total tweets removed")

sns.set_theme(style="whitegrid")
#sns.set_style("ticks")

# ================ Plot with neutral values removed =============
item = sns.catplot(data=tdata_neu_normalized, x="5", y="standardized_compound", kind="box").set(xlabel="Cluster ID", ylabel="Standardized VADER Compound Sentiment Score")
plt.savefig("std_sentiment_box_zero_excl.png", dpi=300)
plt.show()
plt.clf()

# sns.displot(tdata_neu_normalized, x="compound", hue="5", kind="kde", palette="husl").legend.set_title("Cluster ID")
# sns.displot(tdata_neu_normalized, x="compound", hue="5", kind="ecdf", palette="husl").legend.set_title("Cluster ID")
#sns.catplot(data=tdata_neu_normalized, x="5", y="compound", kind="violin")



# Plot the responses for different events and regions
# create timeline of all tweets (Sentiment over time, binned by month)
# sns.lineplot(x="year", y="compound",data=twitter_data, hue="5")
# plt.show()
# plt.clf()

# ============ Plot with neutral included ============
#item = sns.catplot(data=twitter_data, x="5", y="standardized_compound", kind="box").set(xlabel="Cluster ID", ylabel="VADER Compound Sentiment Score")
item = sns.displot(twitter_data, x="compound", hue="5", kind="kde", palette="husl").set(xlabel="Raw VADER Compound Sentiment Score").legend.set_title("Cluster ID")
#item.ax.set_yscale("log")
plt.savefig("std_sentiment_kde_zero_incl.png", dpi=300)
plt.show()








# %%
