import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
font1 = {'family': 'serif',
         'color': 'b',
         'weight': 'bold',
         'size': 14
         }

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 피험자 번호 리스트 생성
subject_ids = [f"A{str(i).zfill(2)}" for i in range(1, 44)] + [f"B{str(i).zfill(2)}" for i in range(1, 47)] + [f"C{str(i).zfill(2)}" for i in range(1, 72)] + [f"D{str(i).zfill(2)}" for i in range(1, 50)]

file = 'data.xlsx'
df = pd.read_excel(file)

s1 = '저체중'
s2 = '표준체중'
s3 = '과체중'
weight_types = [s1, s2, s3]

# 식사 시간 데이터를 수치형으로 변환하는 함수
def convert_meal_time_to_numeric(df):
    time_map = {'15분이내': 0, '30분이내': 1, '30분이상': 2}
    df['식사시간'] = df['식사시간'].map(time_map)
    return df

# 체중 유형별 식사 시간을 박스플롯으로 그리는 함수
def plot_meal_time_by_weight(df):
    meal_times = {weight_type: df[df['체중유형'] == weight_type]['식사시간'] for weight_type in weight_types}

    plt.figure(figsize=(10, 6))
    plt.boxplot([meal_times[weight_type] for weight_type in weight_types], labels=weight_types)
    plt.title('체중 유형별 식사 시간', fontsize=16, fontweight='bold')
    plt.xlabel('체중 유형', fontsize=12, labelpad = 15)
    plt.ylabel('식사 시간 (0: 15분 이내, 1: 30분 이내, 2: 30분 이상)')
    plt.savefig("식사시간.png")

# def plot_meal_time_distribution_proportion(df):
#     weight_types = ['저체중', '표준체중', '과체중']
#     meal_times = ['15분이내', '30분이내', '30분이상']

#     results = pd.DataFrame(columns=meal_times, index=weight_types)

#     for weight_type in weight_types:
#         total_count = df[df['체중유형'] == weight_type].shape[0]
#         for time in meal_times:
#             count = df[(df['체중유형'] == weight_type) & (df['식사시간'] == time)].shape[0]
#             proportion = (count / total_count) * 100 if total_count > 0 else 0
#             results.at[weight_type, time] = proportion

#     results.plot(kind='bar', figsize=(10, 6))
#     plt.title('체중 유형별 식사 시간 비율')
#     plt.xlabel('체중 유형')
#     plt.ylabel('비율 (%)')
#     plt.show()

# plot_meal_time_distribution_proportion(df)
df = convert_meal_time_to_numeric(df)
plot_meal_time_by_weight(df)

def print_boxplot_stats(data):
    for weight_type in data.keys():
        values = data[weight_type]
        mean = np.mean(values)
        median = np.median(values)
        lower_25 = np.percentile(values, 25)
        upper_25 = np.percentile(values, 75)

        print(f"{weight_type}:")
        print(f"  평균값: {mean:.2f}")
        print(f"  중앙값: {median:.2f}")
        print(f"  하위 25% 값: {lower_25:.2f}")
        print(f"  상위 25% 값: {upper_25:.2f}")
        print()
