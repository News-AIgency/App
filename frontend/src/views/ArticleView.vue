<template>
  <div class="page-wrapper">
    <div class="textarea-wrapper">
      <h2 class="title">ARTICLE TOPIC</h2>
      <div class="textarea-container">
        <div class="header-container">
          <h3>Title</h3>
          <p class="word-counter">Word count: 000</p>
        </div>
        <textarea id="title-textarea" v-model="title"></textarea
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

    <div class="title-suggestion-wrapper">
      <h2 class="filler"></h2>
      <h3 class="header-container">Title suggestions</h3>
      <button class="title-btn" @click="copyTitle($event)">Priemerné ceny pohonných látok v SR vzrástli o 2 centy za liter</button>
      <button class="title-btn" @click="copyTitle($event)">Ceny benzínov a nafty zaznamenali najvyššiu hodnotu od septembra</button>
      <button class="title-btn" @click="copyTitle($event)">Spotrebitelia platili za motorovú naftu v priemere 1,420 eura za liter</button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      title: "",
    };
  },
  methods: {
    copyTitle(event: MouseEvent) {
      const target = event.target as HTMLButtonElement;
      this.title = target.textContent || "";
    }
  },
}
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
.page-wrapper {
  margin: auto;
  display: flex;
  width: 95%;
  gap: 0 px;
  justify-content: flex-end;
  flex-direction: row;
  color: var(--color-text);
}

.filler {
  padding: 25.5px;
}

.title-btn {
  background-color: rgba(56, 56, 62, 0.75);
  color: rgba(255, 255 ,255, 0.5);
  border: 0px;
  border-radius: 5px;
  padding: 8px;
  text-align: left;
  cursor: pointer;
  margin-bottom: 10px;
}

.title-btn:hover {
  background-color: rgba(76, 76, 83, 0.75);
  color: white;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.textarea-container textarea {
  width: 100%;
}

.title-suggestion-wrapper {
  display: flex;
  width: 30%;
  flex-direction: column;
}

.textarea-wrapper {
  display: flex;
  width: 50%;
  flex-direction: column;
  margin-right: 2%;
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
  cursor: pointer;

  transition: box-shadow 0.4s ease;

}
.export-button:hover {
  box-shadow: 0 0 8px #9F00FF;
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

h3 {
  font-weight: 600;
}

#perex-textarea {
  height: 6em;
}
#body-textarea {
  height: 25em;
}
</style>
