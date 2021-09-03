from logging import raiseExceptions
import pandas as pd
import DFandFileConverter



# global curr_no_of_coins 
curr_no_of_coins = 5.00

# global curr_account_balance_usd 
curr_account_balance_usd = 5.00

# global total_value_at_start 
total_value_at_start = 0




def execute_sell( curr_price):
    global curr_account_balance_usd
    global curr_no_of_coins 
    no_of_coins_to_sell = float(curr_no_of_coins / 2)
    money_made_by_selling = float(no_of_coins_to_sell * curr_price)
    curr_no_of_coins = curr_no_of_coins - no_of_coins_to_sell
    curr_account_balance_usd = curr_account_balance_usd + money_made_by_selling
    return curr_account_balance_usd , curr_no_of_coins


def execute_buy(curr_price):
    global curr_account_balance_usd
    global curr_no_of_coins 
    amount_in_dollars_to_buy = float(curr_account_balance_usd / 2)
    coins_made_by_buying = float(amount_in_dollars_to_buy / curr_price)
    curr_no_of_coins = curr_no_of_coins + coins_made_by_buying
    curr_account_balance_usd = curr_account_balance_usd - amount_in_dollars_to_buy
    return curr_account_balance_usd , curr_no_of_coins


def total_profit_till_now(curr_price):
    total_value_till_now = float(((curr_no_of_coins * curr_price) + curr_account_balance_usd))
    profit_till_now = total_value_till_now - total_value_at_start
    profit_percent_till_now = float(((profit_till_now / total_value_at_start) * 100 ))
    return total_value_till_now , profit_till_now , profit_percent_till_now


def execute_buy_sell(trade , curr_price , coinname , date_time):

    profit_loss_file = pd.read_csv(coinname+'_profit_loss_file.csv')


    if trade == 'BUY':
        curr_account_balance_usd , curr_no_of_coins =  execute_buy(curr_price)
    elif trade == 'SELL':
        curr_account_balance_usd , curr_no_of_coins = execute_sell(curr_price)    
    else :
        raiseExceptions("NOT BUY/SELL AS TRADE OPTION WAS PASSED")    

    total_value_till_now , profit_till_now , profit_percent_till_now = total_profit_till_now(curr_price)
    
    
    ###
    df = pd.DataFrame([])
    df['TRADE'] = [trade]
    df['CURR-PRICE'] = [curr_price]
    df['COIN-NAME'] = [coinname]
    df['DATE-TIME'] = [date_time]
    df['CURR-NO-OF-COINS-ACC-BALANCE'] = [curr_no_of_coins]
    df['CURR-USD-ACC-BALANCE'] = [curr_account_balance_usd]
    df['TOTAL-VALUE-TILL-NOW'] = [total_value_till_now]
    df['PROFIT-TILL-NOW'] = [profit_till_now]
    df['PROFIT-PERCENT-TILL-NOW'] = [profit_percent_till_now]
    ###

    df.to_csv(coinname+'_profit_loss_file.csv' , mode='a', header=False , index=False)



def make_profit_loss_file(coinname , curr_price , datetime):
     
    initial_curr_price , initial_datetime = curr_price  ,datetime
    
    global total_value_at_start
    total_value_at_start = float(((curr_no_of_coins * initial_curr_price) + curr_account_balance_usd))
    df = pd.DataFrame([])
    df['TRADE'] = ['-']
    df['CURR-PRICE'] = [initial_curr_price]
    df['COIN-NAME'] = [coinname]
    df['DATE-TIME'] = [initial_datetime]
    df['CURR-NO-OF-COINS-ACC-BALANCE'] = [curr_no_of_coins]
    df['CURR-USD-ACC-BALANCE'] = [curr_account_balance_usd]
    df['TOTAL-VALUE-TILL-NOW'] = [0]
    df['PROFIT-TILL-NOW'] = [0]
    df['PROFIT-PERCENT-TILL-NOW'] = [0]

    DFandFileConverter.dfToFilenoindex(df , coinname+'_profit_loss_file.csv')
    
    

