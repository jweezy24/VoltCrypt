import psycopg2
schemea = '''CREATE TABLE keylogKey1 (
    key             int,           
    time            int,           
    instance        int UNIQUE            
); '''

schemea2 = '''CREATE TABLE keylogKey2 (
    key             int,           
    time            int,           
    instance        int UNIQUE            
); '''

schemea10 = '''CREATE TABLE keylogKey1_32bit (
    key             bigint,           
    time            int,           
    instance        int UNIQUE            
); '''

schemea11 = '''CREATE TABLE keylogKey2_32bit (
    key             bigint,           
    time            int,           
    instance        int UNIQUE            
); '''

schemea3 = '''CREATE TABLE rawBufferPreVk1 (
    vkey            int,
    bufferValue     int,          
    time            int,           
    instance        int,
    iter            int            
); '''

schemea4 = '''CREATE TABLE rawBufferPreVk2 (
    vkey            int,
    bufferValue     int,          
    time            int,           
    instance        int,
    iter            int            
); '''

schemea5 = '''CREATE TABLE rawBufferPostVk1 (
    vkey            int,
    bufferValue     int,          
    time            int,           
    instance        int,
    iter            int            
); '''

schemea6 = '''CREATE TABLE rawBufferPostVk2 (
    vkey            int,
    bufferValue     int,          
    time            int,           
    instance        int,
    iter            int            
); '''


def write_to_table(key, epoch, vkey, instance):
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    if vkey == "vk1":
        cur.execute(f"INSERT INTO keylogKey1 (key, time, instance) VALUES ({key}, {epoch}, {instance});")
    elif vkey == "vk2":
        cur.execute(f"INSERT INTO keylogKey2 (key, time, instance) VALUES ({key}, {epoch}, {instance});")
    else:
        print("TABLE NOT FOUND")
    conn.commit()
    cur.close()
    conn.close()

def write_to_table_big(key, epoch, vkey, instance):
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    if vkey == "vk1":
        cur.execute(f"INSERT INTO keylogKey1_32bit (key, time, instance) VALUES ({key}, {epoch}, {instance});")
    elif vkey == "vk2":
        cur.execute(f"INSERT INTO keylogKey2_32bit (key, time, instance) VALUES ({key}, {epoch}, {instance});")
    else:
        print("TABLE NOT FOUND")
    conn.commit()
    cur.close()
    conn.close()


def get_raws_single_instance(instance):

    querey1 = f"select * from rawbufferpostvk1 where instance = {instance} order by iter asc;"
    querey2 = f"select * from rawbufferpostvk2 where instance = {instance} order by iter asc;"

    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()

    cur.execute(querey1)
    key1 = cur.fetchall()

    cur.execute(querey2)
    key2 = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return (key1,key2)

def get_raws_range(low, high):

    querey1 = f"select * from rawbufferpostvk1 where instance > {low} and instance < {high} order by iter asc;"
    querey2 = f"select * from rawbufferpostvk2 where instance > {low} and instance < {high} order by iter asc;"

    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()

    cur.execute(querey1)
    key1 = cur.fetchall()

    cur.execute(querey2)
    key2 = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return (key1,key2)
    

def get_next_instance(vkey,b32=False):
    ret = 0
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    if not b32:
        if vkey == "vk1":
            querey = f'''SELECT instance 
                    FROM  keylogKey1
                    ORDER BY instance DESC 
                    LIMIT 1; '''
            cur.execute(querey)
        elif vkey == "vk2":
            querey = f'''SELECT instance 
                    FROM  keylogKey2
                    ORDER BY instance DESC 
                    LIMIT 1; '''
            cur.execute(querey)
        else:
            print("TABLE NOT FOUND")
    if b32:
        if vkey == "vk1":
            querey = f'''SELECT instance 
                    FROM  keylogkey1_32bit
                    ORDER BY instance DESC 
                    LIMIT 1; '''
            cur.execute(querey)
            key1 = 
        elif vkey == "vk2":
            querey = f'''SELECT instance 
                    FROM  keylogkey2_32bit
                    ORDER BY instance DESC 
                    LIMIT 1; '''
            cur.execute(querey)
        else:
            print("TABLE NOT FOUND")
    ret = cur.fetchone()[0]+1
    conn.commit()
    cur.close()
    conn.close()
    return ret


def get_next_instance_electricity(vkey):
    ret = 0
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    if vkey == "vk1":
        querey = f''' select instance from rawbufferpre where vkey = 1 order by instance desc; '''
        cur.execute(querey)
    elif vkey == "vk2":
        querey = f''' select instance from rawbufferpre where vkey = 2 order by instance desc; '''
        cur.execute(querey)
    else:
        print("TABLE NOT FOUND")
    ret_pre = cur.fetchone()[0]
    print(ret_pre)

    if vkey == "vk1":
        querey = f''' select instance from rawbufferpost where vkey = 1 order by instance desc; '''
        cur.execute(querey)
    elif vkey == "vk2":
        querey = f''' select instance from rawbufferpost where vkey = 2 order by instance desc; '''
        cur.execute(querey)
    else:
        print("TABLE NOT FOUND")
    ret_post = cur.fetchone()[0]
    ret = min(ret_pre, ret_post)
    conn.commit()
    cur.close()
    conn.close()
    return ret

def get_all_keys():
    vk1_queuery = ''' select * from keylogKey1_32bit;'''
    vk2_queuery = ''' select * from keylogKey2_32bit;'''
    #formumlates database connection
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    
    cur.execute(vk1_queuery)
    vkey1_data = cur.fetchall()

    cur.execute(vk2_queuery)
    vkey2_data = cur.fetchall()

    ret = (vkey1_data, vkey2_data)
    
    conn.commit()
    cur.close()
    conn.close()
    return ret

def get_all_buffer(name):
    pre_queuery = f' select * from rawbufferpre{name} where instance > 73 order by instance asc;'
    post_queuery = f' select * from rawbufferpost{name} where instance > 73 order by instance asc; '
    #formumlates database connection
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    
    cur.execute(pre_queuery)
    pre_data = cur.fetchall()

    cur.execute(post_queuery)
    post_data = cur.fetchall()

    ret = (pre_data, post_data)
    
    conn.commit()
    cur.close()
    conn.close()
    return ret

def write_to_buffer_table( vkey, epoch, buffer, iter, instance, which_table):
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()
    
    key = -1
    table = "NA"
    
    if "vk1" == vkey:
        key = 1
        table = "vk1"
    elif "vk2" == vkey:
        key = 2
        table = "vk2"
    
    if table == "NA":
        raise ValueError("Unknown Voltkkey")

    if key == 1:
        if which_table == 0:
            cur.execute(f"INSERT INTO rawBufferPre{table} (vkey, bufferValue, time, instance, iter) VALUES ({key}, {buffer}, {epoch}, {instance}, {iter});")
        elif which_table == 1:
            cur.execute(f"INSERT INTO rawBufferPost{table} (vkey, bufferValue, time, instance, iter) VALUES ({key}, {buffer}, {epoch}, {instance}, {iter});")
        else:
            raise ValueError("Incorrect table value")

    if key == 2:
        if which_table == 0:
            cur.execute(f"INSERT INTO rawBufferPre{table} (vkey, bufferValue, time, instance, iter) VALUES ({key}, {buffer}, {epoch}, {instance}, {iter});")
        elif which_table == 1:
            cur.execute(f"INSERT INTO rawBufferPost{table} (vkey, bufferValue, time, instance, iter) VALUES ({key}, {buffer}, {epoch}, {instance}, {iter});")
        else:
            raise ValueError("Incorrect table value")
    
    conn.commit()
    cur.close()
    conn.close()

schemea7 = '''CREATE TABLE keygenvk1(
    instance    int,
    bit         int,
    binmean     int,
    absmax      int,
    keybit      int
); '''

schemea8 = '''CREATE TABLE keygenvk2(
    instance    int,
    bit         int,
    binmean     int,
    absmax      int,
    keybit      int
); '''

def write_to_key_gen_table(name, instance, it, mean, abs_max, key_bit):
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()

    cur.execute(f"INSERT INTO keygen{name} (instance, bit, binmean, absmax, keybit ) VALUES ({instance}, {it}, {mean}, {abs_max}, {key_bit});")

    conn.commit()
    cur.close()
    conn.close()

def get_all_keygen_data(name):
    select_all_querey = f"select * from keygen{name} where instance = 2 order by instance asc;"
    conn = psycopg2.connect("dbname=vkey user=jweezy")
    cur = conn.cursor()

    cur.execute(select_all_querey)
    
    keygendata = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return keygendata



if __name__ == "__main__":
    #write_to_table(123, 0, "vk2", 0)
    #print(get_next_instance("vk2"))
    print(get_next_instance_electricity("vk2"))