# Each scene: (scene_id, [narration lines])
LONG = [
 ("cold", [
  "Paris, nineteen twenty-five. In a suite at one of the most expensive hotels in the city, a scrap-metal dealer is about to hand over a small fortune in cash.",
  "In return, he believes he is buying seven thousand tonnes of iron. You may know it better, as the Eiffel Tower.",
  "The man selling it does not work for the government. He does not own the tower. And within the hour, he will be on a train out of France.",
  "This is the true story of the man who sold the Eiffel Tower. And then came back, and tried to sell it again.",
 ]),
 ("title", [""]),
 ("who", [
  "His name, as far as anyone can tell, was Victor Lustig. Born in eighteen ninety, in Austria-Hungary, he spoke several languages, dressed like an aristocrat, and introduced himself as a count.",
  "He was not a count. He was a professional liar, with dozens of aliases, and a talent for one thing above all: working out what a person wanted to believe.",
  "He learned his trade on the ocean liners that crossed the Atlantic, where rich passengers were bored, trapped, and far from anyone who could check a story.",
 ]),
 ("box", [
  "His signature trick was a small mahogany box. Feed in a hundred-dollar bill, he explained, wait a few hours for the chemicals to work, and out would come two.",
  "He would demonstrate it. Real bills came out, because he had loaded them in beforehand. Buyers paid thousands of dollars for the machine. By the time it stopped printing, Lustig was gone.",
  "It was a good living. But in the spring of nineteen twenty-five, in Paris, he opened a newspaper, and found something much bigger.",
 ]),
 ("idea", [
  "The Eiffel Tower was in trouble. It had been built for the eighteen eighty-nine World's Fair, and was never meant to stand forever. Thirty-six years later it was rusting, and the cost of repairing and repainting it was enormous.",
  "The article wondered, half seriously, whether the city might be better off without it. Most readers turned the page. Lustig read it as a business plan.",
 ]),
 ("letter", [
  "First, he had stationery forged, carrying the letterhead of the Ministry of Posts and Telegraphs. He gave himself a title: deputy director general.",
  "Then he wrote to a handful of the biggest scrap-metal dealers in Paris, inviting each of them to a confidential meeting at the Hôtel de Crillon. A place where real ministers really did business.",
 ]),
 ("pitch", [
  "When they arrived, he explained the situation, with great regret. The tower had become too costly to maintain. The government had decided to sell it for scrap. Seven thousand tonnes of iron, to the highest bidder.",
  "There was one condition. The public would be furious. So until the deal was signed, nobody could say a word.",
  "It was the perfect lie. The secrecy that should have warned them, instead made them feel chosen. He even took them to the tower to inspect it, and asked for sealed bids by the next day.",
 ]),
 ("mark", [
  "But Lustig had already chosen his buyer. André Poisson was new to Paris, ambitious, and desperate to be taken seriously by the city's business elite. A deal like this would make his name.",
  "There was one problem. Poisson, or by some accounts his wife, grew suspicious. Why the hotel? Why the hurry? Why all the secrecy?",
  "What Lustig did next, is the reason con men still study him.",
 ]),
 ("bribe", [
  "He asked for a private meeting. And there, he made a confession. He was, he admitted, only a civil servant. He was expected to live well, and he was paid very little. Choosing the winning bid was a great responsibility. Perhaps the two of them could come to an arrangement.",
  "He was asking for a bribe. And Poisson relaxed completely. He had met corrupt officials before. A man fishing for a bribe could only be one thing. A real government official.",
  "Lustig had cured the doubt, by confessing to a smaller crime.",
 ]),
 ("payoff", [
  "Poisson paid. Accounts differ on the exact sum, but it was a fortune: the price of the tower, and the bribe on top. Lustig took the cash, and boarded a train for Vienna.",
  "Then, the story goes, he waited, reading the Paris newspapers every day for news of the scandal. Nothing. No story. No police. Poisson had realised the truth, and was too humiliated to tell anyone.",
 ]),
 ("twice", [
  "So Lustig did something almost nobody would dare. He went back. Same city. Same tower. Same story. A new set of scrap dealers.",
  "This time, one of them went to the police. Lustig slipped away before they could reach him, and sailed for America.",
 ]),
 ("america", [
  "In America, he kept going. He once talked Al Capone into handing him fifty thousand dollars for a scheme. Two months later he handed back every cent, apologising that the deal had fallen through.",
  "Capone, impressed by his honesty, gave him five thousand dollars for his trouble. Which was all Lustig had wanted.",
  "Then he moved into counterfeiting, with a chemist named Tom Shaw. Their fake bills were so good, and so many, that more than a hundred thousand dollars a month was flowing into circulation. Now, federal agents wanted him.",
 ]),
 ("caught", [
  "In May, nineteen thirty-five, a jealous girlfriend made an anonymous phone call, and agents grabbed him on a New York street. A key in his wallet led to a locker in the Times Square subway station. Inside: fifty-one thousand dollars in counterfeit bills, and the plates used to print them.",
 ]),
 ("escape", [
  "He had one trick left. The day before his trial, he tied his bedsheets into a rope, climbed out of a window of the federal detention centre in Manhattan, and lowered himself down the wall.",
  "When people looked up, he pretended to be cleaning the windows. Then he reached the pavement, and ran.",
 ]),
 ("end", [
  "He lasted about a month. They caught him in Pittsburgh, and a judge gave him twenty years on Alcatraz.",
  "Victor Lustig died in federal custody, in nineteen forty-seven. The story goes that on his death certificate, under occupation, someone wrote two words. Apprentice salesman.",
  "He never did own the Eiffel Tower. But for one afternoon in Paris, he convinced a man that it was his to sell. And the tower he sold for scrap, is still standing.",
 ]),
 ("outro", [""]),
]
# short: (scene_id, [(narration, caption)])
SHORT = [
 ("s_hook", [("In nineteen twenty-five, a man sold the Eiffel Tower. He didn't own it.", "In 1925, a man sold the Eiffel Tower.|He didn't own it.")]),
 ("s_letter", [("Victor Lustig forged government letterhead, and told Paris scrap dealers the tower was being secretly sold for scrap.", "Victor Lustig forged government letterhead|and told scrap dealers the tower|was secretly being sold for scrap.")]),
 ("s_bribe", [("One buyer got suspicious. So Lustig asked him for a bribe.", "One buyer got suspicious.|So Lustig asked him for a bribe."),
              ("That convinced him. Only a real official would be that corrupt.", "That convinced him.|Only a real official|would be that corrupt.")]),
 ("s_pay", [("He paid. Lustig left for Vienna with the cash. And the buyer was too embarrassed to call the police.", "He paid.|Lustig left for Vienna with the cash.|The buyer was too embarrassed|to call the police.")]),
 ("s_twice", [("So Lustig came back. And tried to sell it again.", "So Lustig came back.|And tried to sell it again.")]),
]

# Three 60-90 s shorts, each its own mini story. None gives away the ending.
SHORTS = {
 "a": [
  ("hook_a", [("In nineteen twenty-five, a man sold the Eiffel Tower. He didn't own it.", "In 1925, a man sold|the Eiffel Tower.|He didn't own it.")]),
  ("cold", None), ("who", None),
  ("cta_a", [("Part two: how he set up the perfect lie. Follow, so you don't miss it.", "Part 2: how he set up|the perfect lie.|Follow so you don't miss it.")]),
 ],
 "b": [
  ("hook_b", [("How do you sell something you don't own? Victor Lustig had a plan.", "How do you sell|something you don't own?|Victor Lustig had a plan.")]),
  ("box", None), ("idea", None), ("letter", None),
  ("cta_b", [("Part three: the meeting where he closed the deal. Follow for part three.", "Part 3: the meeting|where he closed the deal.|Follow for part 3.")]),
 ],
 "c": [
  ("hook_c", [("His buyer was getting suspicious. What the con man did next is still studied today.", "His buyer was|getting suspicious.|What the con man did next|is still studied today.")]),
  ("pitch", None), ("mark", None), ("bribe", None),
  ("cta_c", [("And then, he tried to sell it again. The full case is on the channel.", "And then, he tried|to sell it again.|Full case on the channel.")]),
 ],
}

# Kokoro phoneme fixes for names it says wrong (find with k.tokenizer.phonemize)
PHONEME_FIX = [("lˈʌstɪɡ", "lˈuːstɪɡ"), ("pˈɔɪsən", "pwɑːsˈɔn"), ("kɹˈɪlən", "kɹiːjˈɔn"), ("ændɹˈeɪ", "ɑːndɹˈeɪ")]
