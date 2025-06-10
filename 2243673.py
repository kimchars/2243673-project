import csv
from datetime import datetime
import os

FILE_NAME = 'fridge.csv'

def read_foods():
    foods = []
    try:
        with open(FILE_NAME, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                foods.append(row)
    except FileNotFoundError:
        pass
    return foods

def write_foods(foods):
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'purchase_date', 'expiry_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for food in foods:
            writer.writerow(food)

def add_food(name, purchase_date, expiry_date):
    foods = read_foods()
    foods.append({'name': name, 'purchase_date': purchase_date, 'expiry_date': expiry_date})
    write_foods(foods)
    print(f"✅ {name} 추가 완료!")

def delete_food(name):
    foods = read_foods()
    foods = [food for food in foods if food['name'] != name]
    write_foods(foods)
    print(f"🗑️ {name} 삭제 완료!")

def show_all():
    foods = read_foods()
    if not foods:
        print("냉장고에 저장된 음식이 없습니다.")
        return
    foods.sort(key=lambda x: x['expiry_date'])  # 유통기한 순 정렬
    print("\n📦 전체 음식 목록:")
    for food in foods:
        print(f"{food['name']} | 구매일: {food['purchase_date']} | 유통기한: {food['expiry_date']}")

def check_expiry(days=3):
    foods = read_foods()
    today = datetime.today()
    soon_expiry = []
    expired = []

    for food in foods:
        expiry = datetime.strptime(food['expiry_date'], '%Y-%m-%d')
        diff_days = (expiry - today).days
        if 0 <= diff_days <= days:
            soon_expiry.append((food, diff_days))
        elif diff_days < 0:
            expired.append((food, abs(diff_days)))

    if soon_expiry:
        print("\n⚠️ 유통기한 임박 음식:")
        for food, d in soon_expiry:
            print(f"{food['name']} - {d}일 남음 (유통기한: {food['expiry_date']})")
    else:
        print("\n👌 임박한 음식이 없습니다.")

    if expired:
        print("\n❌ 유통기한 지난 음식:")
        for food, d in expired:
            print(f"{food['name']} - {d}일 지남 (유통기한: {food['expiry_date']})")


def main():
    print("=== 냉장고 음식 유통기한 알리미 ===")
    while True:
        print("\n1. 음식 추가  2. 음식 삭제  3. 전체 보기  4. 유통기한 임박 확인  5. 종료")
        choice = input("선택하세요: ")

        if choice == '1':
            name = input("음식 이름: ").strip()
            purchase_date = input("구매일 (YYYY-MM-DD): ").strip()
            expiry_date = input("유통기한 (YYYY-MM-DD): ").strip()
            add_food(name, purchase_date, expiry_date)

        elif choice == '2':
            name = input("삭제할 음식 이름: ").strip()
            delete_food(name)

        elif choice == '3':
            show_all()

        elif choice == '4':
            check_expiry()

        elif choice == '5':
            print("프로그램 종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == '__main__':
    main()
