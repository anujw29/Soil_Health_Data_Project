A Few Things Before We Start
Before I talk about the whole process, just wanted to say — I didn’t follow the exact “one script” format that was written in the assignment description. I broke the tasks into different parts and handled them separately, mostly because I found it easier to debug and test this way. I’m also someone who constantly refers to documentation for syntax (still not too confident about it) and I’ve used AI a fair bit, mostly for small things like string handling, loop syntax, or pandas functions that didn’t really need logic, just correct formatting.

I also used black for formatting and making the code cleaner and consistent. I had an internship going on at IIT Roorkee at the same time, which made things slightly packed, but this assignment genuinely mattered to me, so I’ve done it, just a bit delayed.

What I Was Trying to Do
The goal was simple: get soil health data from a dynamic government website, consolidate it, transform it, and then do some analysis and generate insights. It sounded straightforward, but in reality, it turned into one of those “everything looks easy until you actually sit down to do it” situations.

The site was dynamic and had cascading dropdowns for state, district, and block. The idea was to automate this and download CSVs for all possible combinations. Then merge and clean those CSVs and finally do some meaningful analysis on them.

How I Approached the Problem -->

I broke the whole thing into three major parts:

Web Scraping (most painful)

Data Consolidation & Transformation

Data Analysis & Insights

Part 1: Web Scraping (a.k.a. Sleepless Night Part 😅)

This part literally took the most time.

I started by trying to use Selenium + Keys from the selenium library to select options in dropdowns — you know, those send_keys() and press enter things. But turns out, that didn’t really work well on this website. The structure was weird and things wouldn’t populate correctly in the next dropdown.

So then I tried a new approach — I scraped all the dropdown values using find_elements_by_xpath, converted them into a list, and used that list to iterate over all possible states and districts.

Another huge pain was downloading the CSV file — after triggering the download, Selenium would freeze because nothing else visibly changed. I spent a whole day just modifying the logic because I thought the download wasn't happening — turns out, I just had to click in the white space after the download to reset the site’s UI and make it responsive again 😭. Took me so long to notice that tiny thing.

Also, handling timeouts and retries became necessary because some dropdowns failed to load randomly — so I had to put a try/except mechanism and sometimes restart the browser session itself.( There are some edge case type codes which I directly took from GPT as there was no harm in it)

Eventually, I saved all the downloaded files and then arranged them in a proper folder structure by state and district so that later merging could be cleaner.
I tried doing this step in the scraping part itself but got some bugs which I was not able to catch, so better thought to arrange the folders after all the CSVs are downloaded.

Also, I noticed that the CSV file i downloaded after clicking on Micronutrient option was same as the one after I clicked on Macro nutrient option, and it was a merged file with both macro and micro nutrient columns. So, didn's include this funtionality in the scraping code.

Part 2: Data Consolidation & Transformation

Honestly, this part felt very standard — like, you loop through your files, load them as pandas dataframes, and then concatenate everything block-wise and district-wise.
Not much of a challenge here — just set patterns. I removed the block name and village name column as they were of no much use now.

Part 3: Data Analysis & Insights

Also quite basic. I calculated the number of samples in each block by summing the number of soil categories (High, Medium, Low) across nutrients like Nitrogen, Phosphorus, etc.

Some simple visualizations and state/district-level summaries followed. I thought of going deeper — like doing clustering or making a region wise crop suggestion logic but given the time, I kept it straightforward.

At one point, I thought of integrating a GIS map with my analysis, which would’ve been cool. But that’s something I’ll definitely try next time I work on such geo-tagged data.

Where and Why I Ran Into Trouble

As I said earlier — scraping dynamic dropdowns was a pain.

The biggest problem was understanding how the page reloads things. Since the dropdowns were nested (i.e. district options load only after state is selected), Selenium couldn’t handle the race conditions well.

The download part too — the part where you need to click on empty white space before moving to the next dropdown — that wasted hours.

Also, initially I tried to save files with raw names, but later realized that names like 577_-_DISTRICT.csv made no sense without context, so I had to rewrite that part.



One of the clean parts was how I wrote functions for:

getting dropdown options,

clicking them,

and saving the CSVs.

It helped to modularize the scraping.

I also had some solid exception handling. For example, if a district failed to load, I added a retry mechanism and skipped the rest rather than crashing the whole loop.(Most of this part I never did earlier, so used different YT videos and AI tools to learn about it)

I saved progress in a log file so that if I stopped or failed midway, I could resume from where I left. That was a huge time-saver.

This was actually a fun learning experience. I had done static web scraping before, but this was my first dynamic site. I learnt a lot about page load handling, state management in Selenium, and also about how important simple things like clicking a white space can be 😅.

Section 2 and 3 were more chill, but the first part definitely taught me patience.

Thanks again, ChatGPT, for helping me with small fixes and syntax queries throughout and BIPP for this cool assignment!
