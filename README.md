# HOFScraper
Determine whether a player should or should not be in the baseball hall of fame
This is one of my first big projects wih Python and I am excited to share it with everyone!
I would really appreciate any feedback on the project.
I am aware that the script is not very efficient and definitely could be done in much faster ways. 
In the future I plan to add much more functionality to make the program run smoother.
Here's what I plan to look at in the future:
1. Making functionality for pitchers to be able
2. Being able to recognize when there is a repeat player
3. Not having to grab the list of players manually from MLB's website
4. Putting more weight into certain stats based on user's preference
5. Combining three separate groupings into one for better code readability
6. Having the already existing Hall of Fame stats be written into an Excel file to drastically make the program faster
7. Much more, (would appreciate any suggestions or help)
All in all, I really enjoyed creating the project and look forward to improving this one and making many more!

Description:
This program determines the averages for batters in the MLB's baseball hall of fame that were inducted from 1990 onward. I used BeautifulSoup to scrape baseball reference's website for the statistics of each player. I placed each of these statistics into two lists, one with the totals from each player and the individual stats. I then calculated the average for each stat and the standard deviation for each stat. The program then asks the user to check for a player and their stats are also grabbed from baseball reference to determine whether or not they belong in the hall of fame. A points system is used to determine their hall of fame worthiness. If a player has stats that are greater than the average, they are rewarded. If the player has stats that are less than the average, they are reprimanded. If a palyer reaches a certain level of points, then that player should be in the hall of fame.
