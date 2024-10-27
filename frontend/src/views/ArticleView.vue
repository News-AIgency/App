<template>
  <div class="page-wrapper">
    <div class="textarea-wrapper">
      <h2 class="title">ARTICLE TOPIC</h2>
      <div class="textarea-container">
        <div class="header-container">
          <h3>Title</h3>
          <p class="word-counter">Word count: 000</p>
        </div>
        <textarea id="title-textarea">
Slovensko zaznamenalo historicky najvyšší rast obnoviteľných zdrojov energie</textarea
        >
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Perex</h3>
          <p class="word-counter">Word count: 000</p>
        </div>
        <textarea id="perex-textarea">
V roku 2023 Slovensko dosiahlo rekordný nárast využívania obnoviteľných zdrojov energie, čo predstavuje významný krok smerom k ekologickejšej budúcnosti krajiny.</textarea
        >
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Body</h3>
          <p class="word-counter">Word count: 000</p>
        </div>
        <textarea id="body-textarea">
Slovenská republika v roku 2023 zaznamenala historicky najvyšší rast v oblasti obnoviteľných zdrojov energie, vrátane solárnej a veternej energie. Podľa údajov Ministerstva životného prostredia sa podiel energie z obnoviteľných zdrojov zvýšil o 15 % oproti predchádzajúcemu roku, čo predstavuje najväčší nárast v novodobej histórii krajiny.

Minister životného prostredia Ján Novák v tejto súvislosti uviedol, že Slovensko sa rýchlo približuje k svojmu cieľu dosiahnuť 30 % energie z obnoviteľných zdrojov do roku 2030. „Tieto výsledky sú dôkazom, že opatrenia a investície do zelenej energie prinášajú ovocie. Sme na správnej ceste k splneniu našich ekologických záväzkov,“ dodal Novák.

Okrem rastu solárnych elektrární sa rozšírila aj infraštruktúra veternej energie, najmä na západe krajiny, kde vzniklo niekoľko nových veterných fariem. Slovensko tiež pokračuje v budovaní projektov pre zvyšovanie energetickej efektívnosti a znižovanie závislosti od fosílnych palív.
Občania, firmy aj obce čoraz viac využívajú možnosti dotácií na inštaláciu solárnych panelov a iných zariadení na výrobu obnoviteľnej energie. Tento trend prispieva nielen k čistejšiemu životnému prostrediu, ale aj k vytváraniu nových pracovných miest v sektore zelenej energie.</textarea
        >
      </div>
      <div class="action-bar">
        <button class="export-button">Export</button>
      </div>

    </div>

    <div class="suggestion-wrapper">
      <h3>Title suggestions</h3>
      <button>Title #1</button>
      <button>Title #2</button>
      <button>Title #3</button>
    </div>
  </div>
</template>

<style scoped>
html {
  scroll-behavior: smooth;
}
.page-wrapper {
  margin: auto;
  display: flex;
  width: 90%;
  justify-content: flex-end;
  flex-direction: row;
  color: var(--color-text);
}

.action-bar {
  display: flex;
  justify-content: flex-end;
}

.textarea-container textarea {
  width: 100%;
}

.suggestion-wrapper {
  display: flex;
  width: 20%;
  flex-direction: column;
}

.textarea-wrapper {
  display: flex;
  width: 60%;
  flex-direction: column;
  margin-right: 5%;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  margin-top: 2px;
}

.word-counter {
  font-size: 12px;
  opacity: 0.5;
}

.export-button {
  width: 15%;
  background-color: var(--color-accent);
  color: var(--color-text);
  border: 0px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  margin-top: 10px;
  cursor: pointer;

}

.title {
  font-size: 2em;
  font-weight: bold;
  text-align: center;
}

textarea {
  background-color: rgba(56, 56, 62, 0.75);
  border-radius: 5px;
  resize: none;
  outline: none;
  caret-color: white;
  padding: 10px;
  color: var(--color-text);
  border: 2px solid rgb(84, 84, 84);
}

.header-container h3 {
  font-weight: 600;
}

#perex-textarea {
  height: 6em;
}
#body-textarea {
  height: 25em;
}
</style>
