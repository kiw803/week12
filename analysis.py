import pandas as pd


def 정제(df):
    df_clean = df.copy()  # 원본을 보호하기 위해 복사본을 만든다
    print("시작 시 행:", len(df_clean))

    df_clean = df_clean.dropna(subset=["점수"])  # 점수가 비어 있는 행을 삭제한다
    print("빈 칸 제거 후 행:", len(df_clean))

    df_clean = df_clean.drop_duplicates()  # 모든 열이 완전히 같은 중복 행을 하나만 남긴다
    print("중복 제거 후 행:", len(df_clean))

    df_clean["반"] = df_clean["반"].str.strip()  # 반의 앞뒤 공백을 제거한다
    df_clean["과목"] = df_clean["과목"].str.strip()  # 과목의 앞뒤 공백을 제거한다

    점수 = pd.to_numeric(df_clean["점수"], errors="coerce")  # 점수를 숫자로 변환한다
    유효한_점수 = 점수.notna() & 점수.between(0, 100) & (점수 % 1 == 0)
    df_clean = df_clean.loc[유효한_점수]  # 0~100 범위를 벗어나거나 정수가 아닌 점수 행을 삭제한다
    print("유효한 점수 필터 후 행:", len(df_clean))

    df_clean["점수"] = 점수.loc[df_clean.index]
    return df_clean
df = 정제(pd.read_csv("scores_2026.csv"))
print("반 종류:", sorted(df["반"].unique()))
print("과목 종류:", sorted(df["과목"].unique()))

# 반별 점수 평균
반별_평균 = df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

# 과목과 반 기준 점수 평균
과목별_반별_평균 = df.groupby(["과목", "반"])["점수"].mean()
print("과목별 반별 점수 평균:")
print(과목별_반별_평균)

df_수학 = df.loc[df["과목"] == "수학"].copy()
print("수학 과목 필터 후 행:", len(df_수학))

df_1반_90점이상 = df_수학.loc[(df_수학["반"] == "1반") & (df_수학["점수"] >= 90)]
print("1반 90점 이상 행:", len(df_1반_90점이상))


def 반별평균(df):
    반별통계 = df.groupby("반")["점수"].agg(
        개수="size",    
        평균="mean",
        중앙값="median",
        최댓값="max",
    )
    반별통계 = 반별통계.round({"평균": 2, "중앙값": 2, "최댓값": 2})
    print("반별 점수 통계:")
    print(반별통계)

    반별평균_series = 반별통계["평균"]
    return 반별평균_series.to_dict()


반별평균(df)
print(반별평균(df)["1반"])

print(df.groupby("반")["점수"].sum().sum())
print(df["점수"].sum())
print(df.groupby("반")["점수"].count().sum())
print(len(df))

print(df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"])

미니 = 정제(pd.read_csv("mini.csv"))
print( 반별평균( 미니))