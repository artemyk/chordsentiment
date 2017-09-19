This is code to perform the analysis and generate the plots used in 

_The Minor Fall, the Major Lift: Inferring Emotional Valence of Musical Chords through Lyrics_<br>
Artemy Kolchinsky, Nakul Dhande, Kengjeun Park, Yong-Yeol Ahn

First, be sure to make a `data/` and a `figures/` subdirectory in this repository.

Then, download the CSV files provided at 
https://figshare.com/s/0ca9d1bdb8fd67896547 and place them into the `data/` directory.

Finally, to generate figures, run the `*.ipy` files using `ipython3`, e.g.
```
ipython3 chordcats.ipy
...
```
All figures will be output to the `figures/` directory.  See the `*.ipy` files for description.

The file `labMT.txt` provides the word-to-happiness dictionary which we use for sentiment analysis. The values were derived by Dodds et al., see http://www.uvm.edu/~cdanfort/research/dodds-danforth-johs-2009.pdf for details.
