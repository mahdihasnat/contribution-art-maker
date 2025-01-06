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

I want to find the formula how github calculates the weight of individual cells. To test that I am going to add 1 commit in first day, 2 commit in second day and so on for 365 days of 2017.
Yes I pushed 66,795 commits to my private repo. But apparently github only counted last 1000 commits for 2017.
![image](https://github.com/user-attachments/assets/196fbd51-d5bc-48cc-87b0-7d9ea4b796af)

I was wondering where is the color lavel decision taken? I checked the network tab and saw this tag comes from server. So the decision code is in the server. 

![image](https://github.com/user-attachments/assets/c804abc3-0322-4300-872c-34d44c5f7ec4)

I will just need to test for few days. So now I will test for 20 days. There will be (1 + 2 + 3 + .. + 43) = 43 * 44 / 2 = 43 * 22 = 946 contributions [ yay it is less than 1000].

![image](https://github.com/user-attachments/assets/f2912074-f88f-4083-b5c7-e6ada0249f2a)
| Level   | Range (out of 43) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 10   | 10 |
| Level-2 | 11 .. 21  | 11 |
| Level-3 | 22 .. 32  | 11 |
| Level-4 | 33 .. 43  | 11 |
----------------------------
![image](https://github.com/user-attachments/assets/cc76a61e-5c2d-4d59-9fa3-218a0b38ff0e)
| Level   | Range (out of 44) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 11   | 11 |
| Level-2 | 12 .. 22  | 11 |
| Level-3 | 23 .. 33  | 11 |
| Level-4 | 34 .. 44  | 11 |
----------------------------
![image](https://github.com/user-attachments/assets/15c1e95b-4514-4d75-8d86-e56be8973f0c)
| Level   | Range (out of 42) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 10   | 10 |
| Level-2 | 11 .. 21  | 11 |
| Level-3 | 22 .. 31  | 10 |
| Level-4 | 32 .. 42  | 11 |
----------------------------

