import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 피험자 번호 리스트 생성
subject_ids = [f"A{str(i).zfill(2)}" for i in range(1, 44)] + [f"B{str(i).zfill(2)}" for i in range(1, 47)] + [f"C{str(i).zfill(2)}" for i in range(1, 72)] + [f"D{str(i).zfill(2)}" for i in range(1, 50)]

file = 'data.xlsx'
df = pd.read_excel(file)

s1 = '저체중'
s2 = '표준체중'
s3 = '과체중'
weight_types = [s1, s2, s3]
def cal_data_box(df):
    results = {
        '저체중': [],
        '표준체중': [],
        '과체중': [], 
        }
    days = ['월', '화', '수', '목', '금', '토', '일']

    for weight_type in weight_types:
        df2 = df[df['체중유형']==weight_type]
        for subject_id in subject_ids:
            #피험자가 해당 체중 유형에 해당할 때만 카운트
            if len(df2[df2['피험자번호'] == subject_id]) == 0:
                continue
            cnt = 0
            for day in days:
                # 해당 날짜, 체중 유형, 피험자 번호에 해당하는 데이터 필터링
                subject_df = df2[(df2['요일'] == day) & (df2['피험자번호'] == subject_id)]
                # todo
                cnt += len(subject_df)
            
            cnt = cnt / 7
            results[weight_type].append(cnt)
            
    return results

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


data = cal_data_box(df)

print_boxplot_stats(data)

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
# 박스플롯 그리기
plt.figure(figsize=(10, 6))
plt.boxplot([data[s1], data[s2], data[s3]], labels=[s1, s2, s3])
plt.title('체중 유형별 일 평균 식사 횟수', fontsize=16, fontweight='bold')
plt.xlabel('체중 유형', fontsize=12, labelpad = 15)
plt.ylabel('일 평균 식사 횟수 (단위: 회)', fontsize=12)
# plt.show()
plt.savefig('일일식사횟수.png')


# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

# # 예제 데이터 생성
# np.random.seed(0)  # 일관된 결과를 위한 랜덤 시드 설정
# data = {
#     '과체중': np.random.randint(1, 6, 1050),  # 1회부터 5회까지 식사하는 경우를 100개 생성
#     '저체중': np.random.randint(1, 6, 50),
#     '표준체중': np.random.randint(1, 6, 100)
# }

# # 박스플롯 그리기
# plt.figure(figsize=(10, 6))
# plt.boxplot([data['과체중'], data['저체중'], data['표준체중']], labels=['과체중', '저체중', '표준체중'])
# plt.title('체중 유형별 일일 식사 횟수')
# plt.xlabel('체중 유형')
# plt.ylabel('일일 식사 횟수')
# plt.show()