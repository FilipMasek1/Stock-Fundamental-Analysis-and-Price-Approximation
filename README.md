## Stock Fundamental Analysis & Price Approximation (SFAPA)

Aplikace pro fundamentální analýzu akcií a aproximaci vývoje jejich ceny pomocí polynomické regrese s grafickým uživatelským rozhraním (GUI) v Pythonu.

### Popis aplikace
**Stock Fundamental Analysis & Price Approximation** je aplikace, která kombinuje vyhodnocování základních finančních ukazatelů společností s analýzou cenových trendů. 

Aplikace funguje ve dvou režimech:
- **Online režim (`Real Analysis Mode`):** Stahuje aktuální finanční data a historické ceny přímo z rozhraní Yahoo Finance (`yfinance`).
- **Offline režim (`Mock Analysis Mode`):** Pokud není dostupné připojení k internetu nebo selže API, aplikace automaticky přepne na lokálně uložená CSV data.

### Funkce

- **Hodnocení fundamentálních metrik:** Automatické posouzení 9 klíčových ukazaželů finančního zdraví firmy vůči cílovým hodnotám.
- **Barevná tabulka:** Generuje přehlednou tabulku stavu metrik.
- **Aproximace ceny polynomem:** Prokládá historický vývoj ceny akcie polynomickou křivkou 3. stupně.
- **Záloha dat pro offline použití:** Možnost stáhnout a uložit získaná data do složky pro pozdější práci bez připojení k internetu.
- **Interaktivní GUI (Tkinter):** Jednoduché grafické rozhraní.

### Práce s aplikací:
Aplikace vyžaduje nainstalovaný Python verze 3.8 nebo vyšší. 

Požadované knihovny nainstalujete příkazem v terminálu / příkazové řádce: 
  **`pip install requirements.txt`

V rámci programu je využíván prohlížeč (Chrome/Chromium). Je proto třeba jej mít nainstalovaný.


1. Aplikaci spustíte příkazem **`python -m app.sfapa` ve složce app
2. **Zadání tickerů:** Do textového pole zadejte symboly akcií oddělené čárkou (a mezerou) (např. `AAPL, MSFT, GOOGL, NVDA`).
3. **Volba období a intervalu:** Vyberte časový horizont a interval pro analýzu dat.
4. **Výběr metrik:** Zaškrtněte metriky, které chcete zobrazit a vyhodnotit v tabulce.
5. **Uložení dat (volitelné):** Zaškrtněte možnost stažení dat, pokud chcete nová data uložit pro offline použití.
6. **Analýza:** Klikněte na tlačítko **Analýza**.
7. **Zobrazení výsledků:** V novém okně se zobrazí barevná tabulka metrik a rozbalovací nabídka pro zobrazení cenového grafu s aproximovanou polynomickou křivkou pro jednotlivé akcie.

### Používané metriky a jejich vysvětlení

Aplikace posuzuje finanční zdraví společností podle 9 základních metrik:

1. **`returnOnEquity` (Návratnost vlastního kapitálu – ROE)**
   - **Cílová hodnota:** $\ge 15\,\%$ (`0.15`)
   - **Vysvětlení:** Měří ziskovost firmy vzhledem k kapitálu vkládanému akcionáři (`Čistý zisk / Vlastní kapitál`). Vyšší ROE značí efektivní zhodnocování kapitálu vedením firmy.

2. **`grossMargins` (Hrubá marže)**
   - **Cílová hodnota:** $\ge 40\,\%$ (`0.40`)
   - **Vysvětlení:** Podíl tržeb, který firmě zůstane po odečtení přímých nákladů na výrobu či prodej zboží (`(Tržby - Přímé náklady) / Tržby`). Odráží cenovou sílu a efektivitu výroby.

3. **`operatingMargins` (Provozní marže)**
   - **Cílová hodnota:** $\ge 15\,\%$ (`0.15`)
   - **Vysvětlení:** Procento tržeb zbývající po zaplacení přímých výroby i provozních nákladů (mzdy, výzkum a vývoj, režie). Ukazuje základní provozní efektivitu.

4. **`profitMargins` (Čistá zisková marže)**
   - **Cílová hodnota:** $\ge 10\,\%$ (`0.10`)
   - **Vysvětlení:** Konečný podíl čistého zisku z celkových tržeb po odečtení všech provozních nákladů, úroků, daní a dividend (`Čistý zisk / Tržby`).

5. **`debtToEquity` (Míra zadluženosti – D/E)**
   - **Cílová hodnota:** $\le 1.5$ (`150 %`)
   - **Vysvětlení:** Poměr celkového dlužení vůči vlastnímu kapitálu akcionářů. Hodnoty pod 1.5 značí konzervativní strukturu financování s nižším rizikem.

6. **`currentRatio` (Běžná likvidita)**
   - **Cílová hodnota:** $\ge 1.5$
   - **Vysvětlení:** Schopnost firmy hradit své krátkodobé závazky (`Oběžná aktiva / Krátkodobé závazky`). Hodnota nad 1.5 garantuje bezproblémové krytí dluhů splatných do jednoho roku.

7. **`freeCashflow` (Volný peněžní tok – FCF)**
   - **Cílová hodnota:** $> 0$
   - **Vysvětlení:** Reálný objem financí, který firmě zůstane po zaplacení provozních a kapitálových výdajů (CapEx). Kladné FCF umožňuje investice, výplatu dividend nebo splácení dluhů.

8. **`trailingPE` (P/E – Historické)**
   - **Cílová hodnota:** $\le 25$
   - **Vysvětlení:** Poměr aktuální ceny akcie k dosaženému zisku na akcii (EPS) za posledních 12 měsíců (TTM). Nižší hodnota může signalizovat výhodnou cenu akcie.

9. **`forwardPE` (P/E – Očekávané)**
   - **Cílová hodnota:** $\le 20$
   - **Vysvětlení:** Poměr ceny akcie k odhadovanému zisku na akcii v následujících 12 měsících. Pomáhá posoudit ocenění akcie vůči budoucímu očekávanému růstu.
