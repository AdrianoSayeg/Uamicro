prueba={
        f'{i}{j}': 0x3+0x1000*(1-j)+0x200*j if f'{i}{j}' in ('00','01')
        else 0x2+0x2000*(3-j)+0x100*(j-2) if f'{i}{j}' in ('02','03')
        else 0x203 if f'{i}{j}' in ('04','05')
        else 0x0 
        for i in ['0','f'] for j in range(6)
    }   
print(', \n'.join(f"{k}: {v:016b}" for k, v in prueba.items()))