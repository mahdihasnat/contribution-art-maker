# contribution-art-maker
Attempt to create nice contribution art 

## Motivation
I came accross to a linkdein post where an author shared nice doller sign in his github contribution chart.

![image](https://github.com/user-attachments/assets/06377e6d-6d3c-4304-b24e-0e101c273c79)

This caught my eyes and being a git enthusiast, I was wondering if I could also draw some art here. This will be very long and painfull process (maybe not that painfull but preparing for worst).

## Idea
As per contribution calculation logic [link](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile), I can just create commits for specific date and contribution points will be added on that day (*utc only*). 

Now I can just run a cron job everyday. That job will commit appropriate number of commit in some private repo. But after just one google search, I found a repo that generate contribution in the **past!** [github-activity-generator](https://github.com/Shpota/github-activity-generator)

I am not surprized because it is possible to spoof commit data. I had a similar experiment here [childhood-codes](https://github.com/mahdihasnat/childhood-codes). I just created a commit for year 2004.

Contribution graph is generated for a year. There are 7 rows. Row starts at sunday. There will be 365[+1 if leap year] data points. Each cell can contain one of the 5 different color. From black to green. 

So my contribution for year 2017 is completely empty:
![image](https://github.com/user-attachments/assets/168a9d23-d487-4b99-9d41-5af0518240a6)

I want to find the formula how github calculates the weight of individual cells. To test that I am going to add 1 commit in first day, 2 commit in second day and so on for  365 days of 2017.

