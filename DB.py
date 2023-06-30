import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()




    def user_exists(self, users_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (users_id,))
        return bool(len(result.fetchall()))
    
    def num_of_users(self):
        self.cursor.execute("SELECT max(rowid) from users")
        nums_users = self.cursor.fetchone()[0]
        return nums_users
    
    def add_user(self, users_id, nick):
        self.cursor.execute("INSERT INTO `users` (`user_name`, `user_id`) VALUES (?, ?)", (nick, users_id))
        return self.conn.commit()
    
    def game_field(self, users_id, game_field):
        self.cursor.execute('''UPDATE users SET game_field = ? WHERE user_id = ?''', (game_field, users_id))
        return self.conn.commit()
    
    def enemy_id(self, enemy_id, users_id):
        self.cursor.execute('''UPDATE users SET enemy_id = ? WHERE user_id = ?''', (enemy_id, users_id))
        return self.conn.commit()
    
    def enemy_message_id(self, enemy_message_id, users_id):
        self.cursor.execute('''UPDATE users SET enemy_message_id = ? WHERE user_id = ?''', (enemy_message_id, users_id))
        return self.conn.commit()
    
    def enemy_search(self, enemy_search, users_id):
        self.cursor.execute('''UPDATE users SET enemy_search = ? WHERE user_id = ?''', (enemy_search, users_id))
        return self.conn.commit()
    
    def figure(self, figure, users_id):
        self.cursor.execute('''UPDATE users SET figure = ? WHERE user_id = ?''', (figure, users_id))
        return self.conn.commit()
    
    def turn(self, turn, users_id):
        self.cursor.execute('''UPDATE users SET turn = ? WHERE user_id = ?''', (turn, users_id))
        return self.conn.commit()

    def get_game_field(self, user_id):
        result = self.cursor.execute("SELECT `game_field` FROM `users` WHERE `user_id` = ?", (user_id,))
        gf=[]
        field=result.fetchall()[0]
        field=int(str(field)[1:][:-2])
        for i in range(9):
            gf.append(int(field%pow(10,9-i)/pow(10,8-i)))
        return gf
    
    def get_figure(self, user_id):
        result = self.cursor.execute("SELECT `figure` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()
    
    def get_turn(self, user_id):
        result = self.cursor.execute("SELECT `turn` FROM `users` WHERE `user_id` = ?", (user_id,))
        return int(str(result.fetchall()[0])[1:][:-2])
    
    def get_enemy_message_id(self, user_id):
        result = self.cursor.execute("SELECT `enemy_message_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()
    
    def get_enemy_search(self, id):
        result = self.cursor.execute("SELECT `enemy_search` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchall()
    
    def get_enemy_id(self, user_id):
        result = self.cursor.execute("SELECT `enemy_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()

    def get_user_id(self, id):
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchall()
    



    def close(self):
        self.connection.close()
        
