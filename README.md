# contribution-art-maker
Attempt to create nice contribution art 

## Motivation
I came accross to a linkdein post where an author shared nice doller sign in his github contribution chart.

![image](https://github.com/user-attachments/assets/06377e6d-6d3c-4304-b24e-0e101c273c79)

This caught my eyes and being a git enthusiast, I was wondering if I could also draw some art here. This will be very long and painfull process (maybe not that painfull but preparing for worst).

## Idea
As per contribution calculation logic [link](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile), I can just create commits for specific date and contribution points will be added on that day (*utc only*). 

Now I can just run a cron job everyday. That job will commit appropriate number of commit in some private repo. But after just one google search, I found a repo that generate contribution in the **past!** [github-activity-generator](https://github.com/Shpota/github-activity-generator)

I am not surprised because it is possible to spoof commit data. I had a similar experiment here [childhood-codes](https://github.com/mahdihasnat/childhood-codes). I just created a commit for year 2004.

Contribution graph is generated for a year. There are 7 rows. Row starts at sunday. There will be 365[+1 if leap year] data points. Each cell can contain one of the 5 different color. From black to green. 

So my contribution for year 2017 is completely empty:
![image](https://github.com/user-attachments/assets/168a9d23-d487-4b99-9d41-5af0518240a6)

I want to find the formula how github calculates the weight of individual cells. To test that I am going to add 1 commit in first day, 2 commit in second day and so on for 365 days of 2017.
Yes I pushed 66,795 commits to my private repo. But apparently github only counted last 1000 commits for 2017.
![image](https://github.com/user-attachments/assets/196fbd51-d5bc-48cc-87b0-7d9ea4b796af)

I was wondering where is the color level decision taken? I checked the network tab and saw this tag comes from server. So the decision code is in the server. 

![image](https://github.com/user-attachments/assets/c804abc3-0322-4300-872c-34d44c5f7ec4)

I will just need to test for few days. So now I will test for 43 days. There will be (1 + 2 + 3 + .. + 43) = 43 * 44 / 2 = 43 * 22 = 946 contributions [ yay it is less than 1000].
I tested with few fix max contributions. (eg. 34, 40, 41, 42, 43).

![image](https://github.com/user-attachments/assets/7c1b03ec-0735-42ce-9a81-c102cf10c1ee)
| Level   | Range (out of 34) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 8   | 8 |
| Level-2 | 9 .. 17  | 9 |
| Level-3 | 18 .. 25  | 8 |
| Level-4 | 26 .. 34  | 9 |
----------------------------
![image](https://github.com/user-attachments/assets/385f7f8b-2f74-4bc6-9d73-e9080b9e89f2)
| Level   | Range (out of 40) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 10   | 10 |
| Level-2 | 11 .. 20  | 10 |
| Level-3 | 21 .. 30  | 10 |
| Level-4 | 31 .. 40  | 10 |
----------------------------
![image](https://github.com/user-attachments/assets/466b3267-748e-44b1-b50d-307291672b48)
| Level   | Range (out of 41) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 10   | 10 |
| Level-2 | 11 .. 20  | 10 |
| Level-3 | 21 .. 30  | 10 |
| Level-4 | 31 .. 41  | 11 |
----------------------------
![image](https://github.com/user-attachments/assets/15c1e95b-4514-4d75-8d86-e56be8973f0c)
| Level   | Range (out of 42) | Total |
|---------|-----------|---------------|
| Level-1 | 1 .. 10   | 10 |
| Level-2 | 11 .. 21  | 11 |
| Level-3 | 22 .. 31  | 10 |
| Level-4 | 32 .. 42  | 11 |
----------------------------
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

After analyzing these results I came up with a function to get levels based on contribution.

https://github.com/mahdihasnat/contribution-art-maker/blob/87c3f3bf4e1ddea310e9689ff544830e32e525fa/formula-verifier.js#L1-L26

Though this formula works for ideal cases I generated, but I really should test this formula for other existing pages. So here is a validator function that visits all the cells and validate the level with my implementation. 

https://github.com/mahdihasnat/contribution-art-maker/blob/87c3f3bf4e1ddea310e9689ff544830e32e525fa/formula-verifier.js#L1-L47

I was hoping that this will pass for every year, but alas!. There are exceptions in some year. For example in 2018, I have 3 days with [4,4,1] contributions. Here my formula suggests the levels will be [4,4,2]. But actual levels were [4,4,4]. 🤦

Anyway, I am going to stick to my formula hoping that it will be correct for majority of the cases.

First time when I tried to color every 365 days, I just got color for last few days. To be exact , contribution for last 1000 comiits. So What if instead of single push after all commits, I will push after every 1000 commit. I tried and actually worked! 🎉

![image](https://github.com/user-attachments/assets/73fe208a-55e1-44bf-a2b3-1b1d2f84c16e)

Now I got the secret to arbitrarily add any number of contribution to the year.

![image](https://github.com/user-attachments/assets/5ff0080f-0488-46a7-9267-229d31eca3f0)

This is my current contribution chart for year 2020. There are different contribution for each day. I want to erase all the existing contribution from this chard. Obviously I don't want to temper the commit date of my existing codes. One idea is to make extra commit on each day such that every day has same number of commits. So I tried that with a little bit of script as the following. You can run this script on dev-tools/console on your github profile page and selecting proper year. After you run the js script, a bash script will be downloaded. Just run the bash script at any of your repository. Tip: you should create a private repository so that you can undoe the contributions by deleteing the repository.

https://github.com/mahdihasnat/contribution-art-maker/blob/7cd5227f4545c3be035e86091d769667e7d04b8c/reset-contribution.js#L1-L76

![image](https://github.com/user-attachments/assets/33c1c90b-827a-4529-9665-fad2343118a7)

Voila! what a nice green valley 💚

## Collaboration
This is currently work in progress project. If you find it interesting and want to contribute, you can create issues, pull requests or just email/message me for discussion.
