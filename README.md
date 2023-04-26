<h1 align="center"> Wave-Function-Collapse </h2>
<p align="center">
This is an attempt at creating a wave function collapse in python and pygame. I didn't used ressources to create it so it's not optimised or it might not reflect what a wave function collapse algorithm would do. It stills need some works.
</p>

> I have few ideas of improvements/upgrades/fix which will be listed in Future

## Requirements 
The program requires PyGame, it can be installed like that :
```console
pip install pygame
```
> You can find more information on the website https://www.pygame.org/

## Information
### Dimensions
You can change the dimension of the tiles for the wave function collapse program making it bigger ( and also faster to generate ) or smaller by changing the value of the variable `D` ( use an integer: 
```python
D = 1
```
> It took me ~180s to generate it with D=1 and 6 different types of tiles and 3 "checks" ( see later )

### Rules or conditions
The program is mainly based on these rules. In this dictionary you can create a new "tile" ( I'm going to use this term for the rest of the readme to design the little pixels/squares which are displayed by the program ) by adding a new `key` to `rules`, and then add has a value an array which contains the conditions/rules of this tile, basicaly it defines near which tiles this particular tile can be created. For example the `Really deep water` (5) water one can be created if it is near `Deep water` (4) or itself (5). 

```python
rules = {
    '0':['1','3','0','4'],      #Mid water
    '1':['0','2','1'],          #Sand
    '2':['1','3','2'],          #Grass
    '3':['0','1','2','3','6'],  #Cliff/Rock
    '4':['0','5','4'],          #Deep water
    '5':['4','5'],              #Really deep water
    '6': ['3','6','0']          #Snow/High altitude
}
```

### Colors
Pygame "allows" the program to render the tiles, and you can choose a color for each of them with the dictionary `colors` :
```python
colors = {
    '0': (56,  179, 227),
    '1': (242, 215, 141),
    '2': (108, 194, 50),
    '3': (91,  92,  91),
    '4': (58,  141, 214),
    '5': (25,  61,  143),
    '6': (200, 200, 200)
}
```
> It uses the RGB code

### Prints
The program prints the different steps ( preparation of the array and generation of the tiles using the wave function collapse ). It'll display the time for each of them, here's an example :
```sys
Preparation time : 5.896655 s
Generation progress: [=                   ] 0% 14/960400
Error 14
Generation progress: [=                   ] 0% 393/960400
Error 393
Generation progress: [=                   ] 0% 1372/960400
Error 1372
Generation progress: [=================== ] 99% 960399/960400
Wave function collapse time : 180.973159 s
Generated tiles : 960400
```
> For the readibility I've replaced the progress bar characters, and for more information about the errors, it'll be below 

There's also a part of the prints which are disabled line 115 ( at the time of the first push ) named `Debugging`, which I don't recommend you to enable if you want to do big generations ( it will drastically increase the compilation time ). It's useful even though if you want to learn/see more datas. Here's an example of some lines of it :
```sys
[0, 490, 2]                                   <- The coordinates of the current tile
Left tile rules : ['0', '5', '4']             <- The rules of the tile at the left of the current one
Top tile rules : ['1', '3', '0', '4']         <- The rules of the tile at the top of the current one
Diagonal left tile rules : ['0', '5', '4']    <- The rules of the tile at the top left of the current one
Possible tiles : ['0', '4']                   <- The rules which are common to all of the neighbor tiles
```
> You can also decide to see the value chosen by the program by looking at the value of `c` line 131 ( at the time of the first push )

## Algorithm
This is I believe how a simple wave function collapse algorithm works, so I tried to replicate/create it in python. The main logic behind it is that it will check the neighbor tiles of the current one ( left, top and top left ), in this case it performs 3 "checks". The variable `b` gets the value of each tiles in a specific direction ( look at the function `tileInDir()` for more information, or below if I document it ), this function will return an array like that : [X Position, Y Position, Value]. Then it gets the 3rd element ( or index 2 ) with 
```python
tileInDir(tiles, i, direction)[2]
                              ^^^
```
which is the value of the tile in the specified direction. After this it gets the corresponding rules of this value ( for example 5 has the values 4 and 5, see Rules or conditions). It does this for the 3 directions ( top, left, top left ) and between all these rules, it will search for the ones which are common for the 3 tiles with the function `findCommons()`. For example,
if it has 3 arrays like :
```
[ 0, 1, 2 ]
[    1, 2, 3 ]
[ 0, 1, 2 ]
Returns : 1 and 2
```
> The formatting of the arrays is weird just to make it easier to see

And after storing the values in common, it will take one of them randomly and this value will be used for the current tile. This is the logic behind this line :
```python
b = findCommons(rules[str(tileInDir(tiles, i, 2)[2])], rules[str(tileInDir(tiles, i, 1)[2])], rules[str(tileInDir(tiles, i, 1.5)[2])])
                                             left                                   top                                   top left     
```
It can be changed to get more interesting results, for example it can perform another 3 "checks" variation ( left, top, top right ):
```python
b = findCommons(rules[str(tileInDir(tiles, i, 2)[2])], rules[str(tileInDir(tiles, i, 1)[2])], rules[str(tileInDir(tiles, i, 0.5)[2])])
                                             left                                   top                                   top right
```
> However, using this 3 "checks" versions gives error.
### Errors
Errors will be displayed as red squares on the map ( this way you will still be able to view the result ), and they're printed in the console like this :
```sys
Error ( index of the tile which causes the error in the array tiles )
```
> Observation : errors tend to happen at the top of the generation and way more often with the 3 "checks" ( left, top, top right ), and also with some rules configurations
### Additional Information
I haven't commented the program as the Simple Neural Network Visualizer's one, that's why the readme is more complete, and if you know how to fix errors, improve it or something else, please let me know.

## Future
Here's a list of features which could be added in the future :
- Each tiles can have different spawning probabilities instead of a random choice in the parts with `findCommons()` ( see above ). So this way water could be more present for example, or the probability of water would decrease as the current tile comes closer to the center of the "map", this way it would create a kind of island
- An error fixing algorithm which would consists in checking error positions the possible values in commons ( with the neighbor tiles), and if there's not a single one, take the most repeated values between the different conditions and then check the tiles around and repeat until there's no more error. It would kind of spread around the positions with errors until there's no errors anymore
- See what a 4 "checks" would give as result
- Easier way to switch between the different checks methods and a way to save generations
