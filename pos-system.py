import os
import time
import datetime
import pandas as pd

ITEM_MASTER_CSV_PAT = "./item_master.csv"
RECEIPT_FILE_NAME = "./receipt_{now}.log"
receipt_file_name = RECEIPT_FILE_NAME.format(now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.item_price=price
    
    def get_price(self):
        return self.item_price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        
    # オーダーを登録する
    def add_item_order(self, item_code, item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        print(self.item_order_list)
        
    # オーダー内容表示
    def view_order_list(self):
        number = 1
        self.sum_price = 0
        self.sum_count = 0

        # self.receipt_name = "receipt_.log"
        self.receipt_name = RECEIPT_FILE_NAME

        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")

        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result = self.get_item_data(item_order)
            # resultに入ってこないNoneになっている。
            # print(result)
            self.sum_price += result[1] * int(item_count)
            self.sum_count += int(item_count)
            # オーダー登録された内容
            receipt_data = "{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)

            number += 1

            # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))
        # print("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))

        # おつり計算（お預り金額ー合計金額）
        received_money = input('お預り金額は？　')  
        change_money = int(received_money) - self.sum_price  
        if change_money >= 0:
            print('{} 円のおつりとなります。'.format(change_money))
        else:
            print('お金が足りません。')

    # レシート記録 
    def write_receipt(self,text):
        print(text)
        # with open(receipt_file_path + self.receipt_name,mode = 'a', encoding='utf-8_sig') as f:
        with open(receipt_file_name ,mode = 'a', encoding='utf-8_sig') as f:
            f.write(text + '\n')

    # def view_item_list(self):
        # for item in self.item_order_list:
            # print("商品コード:{}".format(item))
            
    # オーダーcodeから商品内容を取得する
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code == m.item_code:
                # print(m.item_code, m.item_name, m.item_price) 
                return m.item_name,m.item_price

    # オーダーをコンソールから入力
    def input_order(self):
        loop_count = 0
        while loop_count >= 0:
            loop_count =+ 1
            buy_item_code = input('注文の商品コードは？　（0　でオーダー登録を終了します）' )
            if int(buy_item_code) != 0:
                
                check_item_code = self.get_item_data(buy_item_code)
                if check_item_code != None:
                    print("{} が登録されました".format(check_item_code[0]))
                    buy_item_count = input('何個ですか？　')
                    print("{} 個ですね、".format(buy_item_count))
                    self.add_item_order(buy_item_code,buy_item_count)
                else:
                    print("「{}」は商品マスタに存在しません".format(buy_item_code))
                    
            else:
                break

### CVSファイルからマスタ登録
def master_read_csv():
    item_master = []
    item_count = 0

    print('---------- CSVファイルからマスタ登録を開始します。 ----------')
    item_master_df = pd.read_csv('./sample_item_master.csv',dtype = {"item_code":object}) 
    for item_code,item_name,item_price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["item_price"])):
        item_master.append(Item(item_code,item_name,item_price))
        print("{}({})".format(item_name,item_code))
        item_count += 1
    print("{}品の登録を完了しました。".format(item_count))
    print("-------   マスタ登録完了しました。  ----------")
    print(item_master_df)
    return item_master
    
### メイン処理
def main():
    # マスタ登録
    # 下の代入（item_master.append）のところをCSVから登録するようにする。
    item_master = master_read_csv()
    # item_master=[]
    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))

    # for item in item_master:
        # print(item)
    # print(item_master)
    # オーダー登録
    order = Order(item_master)
    # order.add_item_order("001")
    # order.add_item_order("002")
    # order.add_item_order("003")
    
    # オーダー入力
    order.input_order()
    
    # オーダー表示
    order.view_order_list()
    
    # for item in order.item_order_list:
        # print(order.get_item_data(item))
    
if __name__ == "__main__":
    main()