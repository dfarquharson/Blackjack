# Blackjack Simulator
Planning on going to Vegas soon? Slumming it at Mystic Lake?
Getting exotic up in Hinkley? Planning on playing Blackjack?
You definitely shouldn't, because the house always wins!
Don't care what I have to say? Still stubborn about wasting your money?
Want to simulate your strategies in an unrealistic scenario
where the dealer has a randomly generated and infinitely self-shuffling deck?
Then I guess you've stumbled upon the right program!

The Blackjack simulator that you see here simulates games where players have
different static strategies on when to continue to hit and when to stay.
All values, from 0 to 21, are simulated by default. In my many runs of this program,
I've been surprised to find the most common winning hit threshold is quite high,
18 being the most prevalent (which is to say, keep hitting until your hand total is 18 or higher)

## How to make this do stuff
All the interesting things you might want to do to this project are described in make targets in the [Makefile](https://github.com/dfarquharson/blackjack/blob/master/Makefile).
Particularly of note are:
- `make run`
- `make test`
- `make coverage-html`

## Code Coverage Reports
After running `make coverage-html`, a pretty coverage report will appear in an `htmlcov` directory.
Navigate to ./htmlcov/index.html in your browser to see that report. 

## Future Enhancements
- [x] Expand the space of the simulation by increasing total number of games played
- [ ] Intelligently and optimally handle "soft" hands (the presence of Aces in a hand)
- [ ] Allow for probabilistic strategies that slightly vary when to hit/stay (i.e. stay on 15 25% of the time)
- [ ] Explore use of [hypothesis](https://hypothesis.readthedocs.io/en/latest/) to do generative testing
- [ ] Use [bokeh](https://bokeh.pydata.org/en/latest/) and/or [matplotlib](https://matplotlib.org/) to make pretty pictures out of the results.
