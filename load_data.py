import pandas as pd

# 读取 CSV 文件
df_houses = pd.read_csv("london_houses.csv")
df_prices = pd.read_csv("London.csv")

# 查看数据样本
print("📌 房价数据样本:")
print(df_prices.head())

print("\n📌 房屋特征数据样本:")
print(df_houses.head())

# 检查缺失值
print("\n📌 缺失值统计:")
print(df_prices.isnull().sum())
print(df_houses.isnull().sum())

print(df_prices["Location"].unique())  # 使用正确大小写

# 查看 Neighborhood 的唯一值
print("📌 `london_houses.csv` 中的 `Neighborhood` 唯一值:")
print(df_houses["Neighborhood"].unique())

# 查看 Borough 的唯一值
print("\n📌 `London.csv` 中的 `Location` 唯一值:")
print(df_prices["Location"].unique())

# 创建 `Neighborhood` 到 `Borough` 的映射关系
neighborhood_to_location = {
    "Notting Hill": "Kensington and Chelsea",
    "Soho": "Westminster",
    "Marylebone": "Westminster",
    "Camden": "Camden",
    "Shoreditch": "Hackney",
    "Greenwich": "Greenwich",
    "Kensington": "Kensington and Chelsea",
    "Chelsea": "Kensington and Chelsea",
    "Islington": "Islington",
    "Westminster": "Westminster",
    "Wimbledon": "Merton",
    "Putney": "Wandsworth",
    "Clerkenwell": "Islington",
    "Fulham": "Hammersmith and Fulham",
    "Highgate": "Camden",
    "Battersea": "Wandsworth",
    "Hampstead": "Camden",
    "Tooting": "Wandsworth",
    "Canary Wharf": "Tower Hamlets",
    "Ealing": "Ealing",
    "Hackney": "Hackney",
    "Whitechapel": "Tower Hamlets",
    "Mayfair": "Westminster",
    "Fitzrovia": "Camden",
    "Pimlico": "Westminster",
    "South Bank": "Lambeth",
}

# 映射 `Neighborhood` 到 `Location`
df_houses["Mapped_location"] = df_houses["Neighborhood"].map(neighborhood_to_location)

# 检查未匹配的 `Neighborhood`
unmatched = df_houses[df_houses["Mapped_location"].isnull()]["Neighborhood"].unique()
print("❌ 以下 `Neighborhood` 仍然未匹配到 `location`:")
print(unmatched)

df_merged = pd.merge(df_houses, df_prices, left_on="Neighborhood", right_on="Location", how="left")

# 检查合并后的数据
print("📌 合并后数据样本:")
print(df_merged.head())

print("📌 未匹配的 `Neighborhood`（NaN `Location`）:")
print(df_merged[df_merged["Location"].isnull()])

df_merged.to_csv("cleaned_london_data.csv", index=False)
print("✅ 数据清理完成，已保存为 cleaned_london_data.csv")

print("📌 合并后数据的基本信息:")
print(df_merged.info())

print("\n📌 主要数值列的统计信息:")
print(df_merged.describe())

print("\n📌 是否还有缺失值？")
print(df_merged.isnull().sum())



