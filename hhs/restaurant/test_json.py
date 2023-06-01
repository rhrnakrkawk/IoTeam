import json

def read_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error while reading data: {str(e)}")
        return None
    
def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# 데이터 파일 경로
file_path = 'order.json'

# 데이터 파일 읽기
data = read_data(file_path)
food = data["food"]
print(food)
# if data is not None:
#     # 데이터 추가
#     new_item = {'name': 'John', 'age': 30}
#     data.append(new_item)

#     # 데이터 파일 쓰기
#     write_data(file_path, data)

