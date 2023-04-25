import pygame
import random
import time

launched = True
resolution = (980,980)
pygame.init()                  
pygame.display.set_caption('Wave Function Collapse')

window = pygame.display.set_mode(resolution,pygame.NOFRAME,pygame.OPENGL)

D = 1                       #Dimension of the "pixels"

rules = {
    '0':['1','3','0','4'],  #Mid water
    '1':['0','2','1'],      #Sand
    '2':['1','3','2'],      #Grass
    '3':['0','1','2','3','6'],  #Cliff/Rock
    '4':['0','5','4'],      #Deep water
    '5':['4','5'],          #Really deep water
    '6': ['3','6','0']       #Snow/High altitude
}

colors = {
    '0': (56, 179, 227),
    '1': (242, 215, 141),
    '2': (108, 194, 50),
    '3': (91, 92, 91),
    '4': (58, 141, 214),
    '5':(25, 61, 143),
    '6': (200,200,200)
}

def tile(x,y,dimension,v):
    pygame.draw.rect(window,v,(x*dimension,y*dimension,dimension))
    
def tileInDir(arr,index,dir):
    numHorizTiles = int(resolution[0]/D)
    try:
        if dir == 0:                                    #Right
            if index+1 <= len(arr)-1:
                return arr[int(index)+1]
            else : return [0,0,0]
        elif dir == 1:                                  #Top/Up
            if index-numHorizTiles >= 0:
                return arr[int(index)-numHorizTiles]
            else : return [0,0,0]
        elif dir == 2:                                  #Left
            if index-1 >= 0:
                return arr[int(index)-1]
            else : return [0,0,0]   
        elif dir == 3:                                  #Bottom/Down
            if index+numHorizTiles <= len(arr)-1:
                return arr[int(index)+numHorizTiles]
            else : return [0,0,0]
        elif dir == 1.5:                                #Top Left
            if index-numHorizTiles-1 >= 0:
                return arr[int(index)-numHorizTiles-1]
            else : return [0,0,0]
        elif dir == 0.5:                                #Top Right
            if index-numHorizTiles+1 <= len(arr)-1:
                return arr[int(index)-numHorizTiles+1]
            else : return [0,0,0]
        else:
            print('Invalid direction')
            return -1
    except:
        print('Invalid direction or tile not existing')
        return -1

def findCommons(arr1, arr2, arr3):
    a = []
    for i in arr1:
        #print(i)
        for j in arr2:
            #print(j)
            for z in arr3:
                #print(z)
                if i == j == z:
                    a.append(z)
    return(a)   

def progress_bar(current, total, bar_length=20):
    fraction = current / total

    fill = int(fraction * bar_length - 1) * '█'+'█'
    padding = int(bar_length - len(fill)) * '░'

    ending = '\n' if current == total else '\r'

    print(f'Generation progress: {fill}{padding} {int(fraction*100)}% {current}/{total}', end=ending)
    
tiles = []

start = time.time()

for y in range(0,int(resolution[1]/D)):
    
    for x in range(0,int(resolution[0]/D)):
        color = random.randint(0,3)
        pygame.draw.rect(window,(0,0,color*(255/3)),(x*D,y*D,D,D))
        tile = [x*D,y*D,color]
        tiles.append(tile)
        #print(tile)

end = time.time()

print('Preparation time : %f s' %(end-start))

start = time.time()

progress = 0
for i in range(len(tiles)):
    
    """ Debugging
    print('Tile number %d' % i)
    print(tiles[i])

    print('Left tile rules : %s' %rules[str(tileInDir(tiles, i, 2)[2])])
    print('Top tile rules : %s' %rules[str(tileInDir(tiles, i, 1)[2])])
    print('Diagonal left tile rules : %s' %rules[str(tileInDir(tiles, i, 1.5)[2])])

    print('Possible tiles : %s' %findCommons(rules[str(tileInDir(tiles, i, 2)[2])], rules[str(tileInDir(tiles, i, 1)[2])], rules[str(tileInDir(tiles, i, 1.5)[2])]))
    """
    
    progress_bar(progress,len(tiles),20)
    
    b = findCommons(rules[str(tileInDir(tiles, i, 2)[2])], rules[str(tileInDir(tiles, i, 1)[2])], rules[str(tileInDir(tiles, i, 1.5)[2])])

    try: 
        c = b[random.randint(0, len(b)-1)]
        pygame.draw.rect(window,colors[str(c)],(tiles[i][0],tiles[i][1],D,D))
        tiles[i]=[tiles[i][0],tiles[i][1],c]
        
    except:
        print('\nError %i' %i)
        pygame.draw.rect(window,(255,0,0),(tiles[i][0],tiles[i][1],D,D))
    
    progress+=1

end = time.time()

print('\nWave function collapse time : %f s' %(end-start))

print('Generated tiles : %i' %len(tiles))

    

while launched:
    pygame.display.update()
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                launched = False
                pygame.quit()