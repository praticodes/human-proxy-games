# Hanabi Observation Space Interpretation
For simplicity, the table below assumes that the current player viewing the observations is Player 1.

| Index | Description | Size (bits) |
| :--- | :--- | :--- |
| **Other Players' Hands (10 cards)** | | |
| 0 - 24 | Vector of Player 2's Card 1 | 25 |
| 25 - 49 | Vector of Player 2's Card 2 | 25 |
| 50 - 74 | Vector of Player 2's Card 3 | 25 |
| 75 - 99 | Vector of Player 2's Card 4 | 25 |
| 100 - 124 | Vector of Player 2's Card 5 | 25 |
| 125 - 149 | Vector of Player 3's Card 1 | 25 |
| 150 - 174 | Vector of Player 3's Card 2 | 25 |
| 175 - 199 | Vector of Player 3's Card 3 | 25 |
| 200 - 224 | Vector of Player 3's Card 4 | 25 |
| 225 - 249 | Vector of Player 3's Card 5 | 25 |
| **Global Game State** | | |
| 250 - 299 | Unary Encoding of Remaining Deck Size | 50 |
| 300 - 304 | Unary encoding of the highest rank played for the Red firework. | 5 |
| 305 - 309 | Unary encoding of the highest rank played for the Yellow firework. | 5 |
| 310 - 314 | Unary encoding of the highest rank played for the Green firework. | 5 |
| 315 - 319 | Unary encoding of the highest rank played for the White firework. | 5 |
| 320 - 324 | Unary encoding of the highest rank played for the Blue firework. | 5 |
| 325 - 332 | Unary encoding of the number of remaining info (hint) tokens. | 8 |
| 333 - 335 | Unary Encoding of Remaining Life Tokens | 3 |
| 336 - 385 | Thermometer encoding over all 50 cards in the deck indicating which have been discarded. | 50 |
| **Previous Action** | | |
| 386 - 389 | Vector of Previous Player’s Action Type | 4 |
| 390 - 391 | Vector of Target from Previous Action | 2 |
| 392 - 396 | Vector of the Color Revealed in Last Action | 5 |
| 397 - 401 | Vector of the Rank Revealed in Last Action | 5 |
| 402 - 403 | Vector of Which Cards in Hand were Revealed | 2 |
| 404 - 405 | Position of the Card that was played or dropped | 2 |
| 406 - 430 | Vector Representing Card that was last played | 25 |
| **This Player's Hand Knowledge (5 cards)** | Each card's knowledge is a 35-bit vector: 5 bits for a color hint, 5 for a rank hint, and 25 for the AI's belief state. | |
| 431 - 465 | Revealed Info of This Player’s 0th Card | 35 |
| 466 - 500 | Revealed Info of This Player’s 1st Card | 35 |
| 501 - 535 | Revealed Info of This Player’s 2nd Card | 35 |
| 536 - 570 | Revealed Info of This Player’s 3rd Card | 35 |
| 571 - 605 | Revealed Info of This Player’s 4th Card | 35 |
| **Other Players' Hand Knowledge (10 cards)** | See above for the 35-bit structure. | |
| 606 - 640 | Revealed Info of Player 2's 0th Card | 35 |
| 641 - 675 | Revealed Info of Player 2's 1st Card | 35 |
| 676 - 710 | Revealed Info of Player 2's 2nd Card | 35 |
| 711 - 745 | Revealed Info of Player 2's 3rd Card | 35 |
| 746 - 780 | Revealed Info of Player 2's 4th Card | 35 |
| 781 - 815 | Revealed Info of Player 3's 0th Card | 35 |
| 816 - 850 | Revealed Info of Player 3's 1st Card | 35 |
| 851 - 885 | Revealed Info of Player 3's 2nd Card | 35 |
| 886 - 920 | Revealed Info of Player 3's 3rd Card | 35 |
| 921 - 955 | Revealed Info of Player 3's 4th Card | 35 |
| **Total Size** | | **956** |
