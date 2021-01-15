feats = ['BTC', 'Volume']
COMMISSION = 0.001

class Env:
    def __init__(self, df):
        self.df = df
        self.n = len(df)
        self.current_idx = 0
        self.action_space = [0, 1, 2]  # BUY, SELL, HOLD
        self.invested = 0
        self.prev_action = 2  # in this variable will be store the previous actions, prev acction in init is HOLD

        self.states = self.df[feats].to_numpy()
        # ahora el reward esta en la columna BTC
        # Tanto los estados como los returns son la misma columna BTC (log return)
        self.rewards = self.df['BTC'].to_numpy()
        self.total_buy_and_hold = 0

    def reset(self):
        self.current_idx = 0
        self.total_buy_and_hold = 0
        return self.states[self.current_idx]

    def step(self, action):
        # need to return (next_state, reward, done)

        self.current_idx += 1
        if self.current_idx >= self.n:
            raise Exception("Episode already done")

        # update invested
        self.update_invested(action)

        # compute reward
        reward = self.compute_reward(action)

        # state transition
        next_state = self.states[self.current_idx]

        # baseline
        self.total_buy_and_hold += self.rewards[self.current_idx]

        # store previous action
        self.prev_action = action

        done = (self.current_idx == self.n - 1)
        return next_state, reward, done

    # NOW IT HANDLE FUTURES
    # if the trend's direction is up and buy -> sell (the bot win)
    # if the trend's direction is up and sell -> buy (the bot loss)
    # if the trend's direction is down and sell -> buy (the bot win) [the qty es negative but do not matter]
    # if the trend's direction is down and buy -> sell (the bot loss) [the qty es negative but do not matter]
    def compute_reward(self, action):

        # compute reward
        # if self.invested is 1 and rewards is positive then add reward [(reward)*(1)]
        # if self.invested is -1 and rewards is negative then add reward [(-reward)*(-1)]
        # if self.invested is 1 and reward is negative then subtract reward [(-reward)*(1)]
        # if self.invested is negative and reward is positive then remove reward [(reward)*(-1)]
        # if invested is 0 then reward is 0 [(-reward)*0]
        reward = self.rewards[self.current_idx] * self.invested

        # commission = 0
        # # calculate commission
        # if action == 0 or action == 1:  # BUY or SELL
        #     commission = reward * COMMISSION
        #
        # # apply commission to the reward
        # return reward - commission

        return reward

    def update_invested(self, action):
        if action == 0:  # BUY
            if self.invested == -1:
                # SELL -> BUY
                self.invested = 0
            else:
                # HOLD -> BUY
                # BUY -> BUY
                self.invested = 1
        elif action == 1:  # SELL
            if self.invested == 1:
                # BUY -> SELL
                self.invested = 0
            else:
                # HOLD -> SELL
                # SELL -> SELL
                self.invested = -1
