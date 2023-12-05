import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 피험자 번호 리스트 생성
subject_ids = [f"A{str(i).zfill(2)}" for i in range(1, 44)] + [f"B{str(i).zfill(2)}" for i in range(1, 47)] + [f"C{str(i).zfill(2)}" for i in range(1, 72)] + [f"D{str(i).zfill(2)}" for i in range(1, 50)]

file = 'data.xlsx'
df = pd.read_excel(file)

# 데이터 집계 및 비율 계산 함수
def aggregate_food_types_proportion(df):
    food_types = ['한식', '양식', '일식','중식', '인스턴트', '기타']
    weight_types = ['저체중', '표준체중', '과체중']

    # 결과를 저장할 데이터프레임
    aggregated_data = pd.DataFrame(index=food_types, columns=weight_types)

    for weight_type in weight_types:
        # 체중 유형별 전체 식사 횟수
        total_count = df[df['체중유형'] == weight_type].shape[0]

        for food_type in food_types:
            # 체중 유형 및 음식 유형별 식사 횟수
            count = df[(df['체중유형'] == weight_type) & (df['음식유형'] == food_type)].shape[0]
            # 체중 유형별 음식 유형의 비율 계산
            proportion = (count / total_count) * 100 if total_count > 0 else 0
            aggregated_data.at[food_type, weight_type] = proportion

    return aggregated_data

# 데이터 집계 및 비율 계산
aggregated_data = aggregate_food_types_proportion(df)

# # 막대 그래프 그리기
# aggregated_data.plot(kind='bar', figsize=(12, 6))
# plt.title('체중 유형별 섭취하는 음식 유형의 비율')
# plt.xlabel('음식 유형')
# plt.ylabel('비율(%)')
# plt.show()

aggregated_data = aggregated_data.applymap(lambda x: f"{x:.2f}%")


# 표(table)로 시각화
fig, ax = plt.subplots(figsize=(12, 6)) # 그래프 크기 설정
ax.axis('tight')
ax.axis('off')
ax.table(cellText=aggregated_data.values, colLabels=aggregated_data.columns, rowLabels=aggregated_data.index, cellLoc = 'center', loc='center')

plt.savefig("음식유형차이.png")