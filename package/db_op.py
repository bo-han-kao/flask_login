import sqlite3


class Database:
    def __enter__(self):
        self.con = sqlite3.connect('app.db')
        self.cur = self.con.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def set_notify(self, line_uuid, type_, val):
        self.cur.execute(f'''UPDATE user
        SET {type_} = ?
        WHERE Line_uuid = ?''', (val, line_uuid))
        self.con.commit()

    def get_notify(self, line_uuid, type_):
        self.cur.execute(f'''SELECT {type_}
        FROM user
        WHERE Line_uuid = ?''', (line_uuid,))
        return self.cur.fetchone()

    def get_tokens(self, device_mac, device_type, mqtt_dongle_id=None):
        if mqtt_dongle_id is not None:
            self.cur.execute(f'''SELECT NotifyToken
            FROM user
            INNER JOIN notify_status USING (username)
            WHERE mqtt_dongle_id = ? AND Device_Mac = ? AND Device_type = ? AND Device_status = 1''', (mqtt_dongle_id, device_mac, device_type))
        else:
            self.cur.execute(f'''SELECT NotifyToken
            FROM user
            INNER JOIN notify_status USING (username)
            WHERE Device_Mac = ? AND Device_type = ? AND Device_status = 1''', (device_mac, device_type))
        return self.cur.fetchall()

    def get_g1_mac(self, line_uuid):
        self.cur.execute('''SELECT Device_Mac
        FROM notify_status
        INNER JOIN user USING (username)
        WHERE Line_uuid = ? AND Device_type = G1''', (line_uuid,))
        return self.cur.fetchone()

    def save_device_data(self, device_mac, mqtt_dongle_id, device_type):
        self.cur.execute('''INSERT OR IGNORE INTO notify_status
        SELECT username, ?, 1, ?
        FROM user
        WHERE mqtt_dongle_id = ?''', (device_mac, device_type, mqtt_dongle_id))
        self.con.commit()
