import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# グラフの保存先
output_dir = Path("./outputs")

# outputsフォルダがなければ作成
output_dir.mkdir(exist_ok=True)


# ① 家計データを読み込む
df = pd.read_csv("./data/SSDSE-C-2026s.csv")


# ② 項目コードの対照表を読み込む
items = pd.read_csv("./data/koumoku.csv")


# ③ コードと日本語名の対応表を作る
code_to_japanese = dict(
    zip(
        items["項目コード"],
        items["日本語名"]
    )
)

# ④ 家計データの列名を日本語に変更する
df_jp = df.rename(
    columns=code_to_japanese
)

# ⑤ 都道府県・市・チーズの列を表示する
print(
    df_jp[
        ["Prefecture", "City", "チーズ"]
    ].head()
)

cheese = df_jp.loc[
    df_jp["Region_Code"] != "R00000",
    ["Prefecture", "City", "チーズ"]
].copy()

cheese_ranking = cheese.sort_values(
    by="チーズ",
    ascending=False
)

print(cheese_ranking.head(10))

# チーズ支出額が多い都市トップ10
top10 = cheese_ranking.head(10)

# グラフ全体の大きさ
plt.figure(figsize=(10, 6))

# 横向きの棒グラフ
sns.barplot(
    data=top10,
    x="チーズ",
    y="City",
    color="gold"
)

# グラフのタイトルと軸名
plt.title("Top 10 Cities by Annual Cheese Expenditure")
plt.xlabel("Annual Expenditure per Household (Yen)")
plt.ylabel("City")

# 文字が切れないように調整
plt.tight_layout()

# グラフを表示
plt.show()

# チーズ支出額の基本統計量
average = cheese["チーズ"].mean()
median = cheese["チーズ"].median()
maximum = cheese["チーズ"].max()
minimum = cheese["チーズ"].min()

print(f"平均値：{average:,.0f}円")
print(f"中央値：{median:,.0f}円")
print(f"最大値：{maximum:,}円")
print(f"最小値：{minimum:,}円")

# グラフの大きさを決める
plt.figure(figsize=(10, 6))

# チーズ支出額のヒストグラム
sns.histplot(
    data=cheese,
    x="チーズ",
    bins=10,
    color="gold",
    edgecolor="black"
)

# 平均値を赤い点線で表示
plt.axvline(
    average,
    color="red",
    linestyle="--",
    label=f"Average: {average:,.0f} yen"
)

# タイトルと軸名
plt.title("Distribution of Annual Cheese Expenditure")
plt.xlabel("Annual Expenditure per Household (Yen)")
plt.ylabel("Number of Cities")

# 平均値の説明を表示
plt.legend()

# 文字が切れないように調整
plt.tight_layout()

plt.savefig(
    output_dir / "cheese_top10.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    output_dir / "cheese_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.show()

# グラフを表示
plt.show()

# チーズとワインの分析用データ
cheese_wine = df_jp.loc[
    df_jp["Region_Code"] != "R00000",
    ["City", "チーズ", "ワイン"]
].copy()

# 相関係数を計算
correlation = cheese_wine[
    ["チーズ", "ワイン"]
].corr().loc["チーズ", "ワイン"]

print(f"チーズとワインの相関係数：{correlation:.2f}")


# 散布図を作成
plt.figure(figsize=(10, 6))

sns.regplot(
    data=cheese_wine,
    x="ワイン",
    y="チーズ",
    scatter_kws={
        "color": "gold",
        "s": 60,
        "alpha": 0.7
    },
    line_kws={
        "color": "red"
    }
)

plt.title("Relationship Between Wine and Cheese Expenditure")
plt.xlabel("Annual Wine Expenditure per Household (Yen)")
plt.ylabel("Annual Cheese Expenditure per Household (Yen)")
plt.tight_layout()

# グラフを保存
plt.savefig(
    output_dir / "cheese_wine_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()