<template>
  <header>
    <div class="container nav">
      <div class="logo">WR<span class="red">AI</span>TE</div>

      <div class="nav-wrapper">
        <nav id="nav-links">
          <a href="#team">Our team</a>
          <a href="#docs">Docs</a>
          <button class="cta" @click="redirectToHomepage">Try it now</button>
        </nav>

        <div class="hamburger" id="hamburger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="hero-content">
        <h1>WR<span class="red">AI</span>TE</h1>
        <p>Generate news articles from verified sources with AI</p>
      </div>

      <button class="cta" @click="redirectToHomepage">Try it now <span class="arrow">→</span></button>
    </section>

    <section class="screenshot">
      <img
        class="screenshot-img"
        src="../assets/images/screenshot_homepage.png"
        alt="App Screenshot Placeholder"
      />
    </section>

    <section id="team" class="team">
      <h2>Our Team</h2>
      <div class="team-grid">
        <!-- Repeat for all 6 team members -->
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/mr_scraper.png"
              alt="MR Scraper "
              width="100%"
              height="100%"
            />
          </div>
          <h3>Jakub Grúber</h3>
          <div class="tags">
            <span>Scraping</span><span>AI</span><span>Backend</span>
          </div>
        </div>
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/smitomic.jpg"
              alt="MR AI "
              width="100%"
              height="100%"
            />
          </div>
          <h3>Tomáš Tomčány</h3>
          <div class="tags"><span>AI</span><span>Backend</span></div>
        </div>
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/mr_sekjuriti.jpg"
              alt="MR AI "
              width="100%"
              height="100%"
            />
          </div>
          <h3>Jakub Gašparín</h3>
          <div class="tags"><span>Database</span><span>Security</span></div>
        </div>
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/totes.jpg"
              alt="MRS UX "
              width="100%"
              height="100%"
            />
          </div>
          <h3>Maria Fedosenya</h3>
          <div class="tags"><span>Frontend</span><span>UI/UX</span></div>
        </div>
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/justvibe.png"
              alt="MR AI "
              width="100%"
              height="100%"
            />
          </div>
          <h3>Patrik Hitka</h3>
          <div class="tags">
            <span>Vibe Coder</span><span>AI</span><span>Backend</span>
          </div>
        </div>
        <div class="team-member">
          <div class="avatar">
            <img
              src="../assets/images/MR_DevOps.jpg"
              alt="MR DevOps Sexy Face"
              width="100%"
              height="100%"
            />
          </div>
          <h3>Ľubor Koka</h3>
          <div class="tags"><span>DevOps</span><span>Frontend</span></div>
        </div>
      </div>
      <div class="email-container">
        <p class="team-email">Team email:</p>
        <a class="email-link" href="mailto:tptim042024@gmail.com"
          >tptim042024@gmail.com</a
        >
      </div>
    </section>

    <section id="docs" class="docs">
      <h2>Docs</h2>
      <div class="doc-item">
        <div class="doc-left">
          <div class="doc-date">11.11.2024</div>
          <div>Zapisnica č.1</div>
        </div>
        <a href="#" class="download-btn">Download</a>
      </div>
      <div class="doc-item">
        <div class="doc-left">
          <div class="doc-date">11.11.2024</div>
          <div>Zapisnica č.2</div>
        </div>
        <a href="#" class="download-btn">Download</a>
      </div>
      <div class="doc-item">
        <div class="doc-left">
          <div class="doc-date">11.11.2024</div>
          <div>Zapisnica č.3</div>
        </div>
        <a href="#" class="download-btn">Download</a>
      </div>
    </section>
  </main>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';

export default {
  name: 'TeamPageView',
  setup() {
    const router = useRouter();

    const hamburger = document.getElementById('hamburger')
    const navLinks = document.getElementById('nav-links')

    if (hamburger && navLinks) {
      hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('show')
        hamburger.classList.toggle('active')
      })
    }
    return {router};
  },
  methods: {
    redirectToHomepage() {
      this.router.push('/');
    },
  },


}




</script>

<style scoped>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #f9f9f9;
    color: #111;
  }

  a {
    color: inherit;
    text-decoration: none;
  }

  header {
    background: #fff;
    border-bottom: 1px solid #eee;
    padding: 1rem 2rem;
  }

  .container.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav-links {
    display: flex;
    gap: 1.5rem;
  }

  .logo {
    font-weight: 900;
    font-size: 1.5rem;
  }

  .logo .red {
    color: red;
  }

  .red {
    font-weight: 900;
  }

  nav {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  nav.show {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 60px;
    right: 0;
    background: white;
    width: 100%;
    padding: 1rem;
    box-shadow: 0 5px 10px rgba(0,0,0,0.1);
  }

  h2 {
    font-weight: 700;
  }

  h3 {
    font-weight: 600;
  }

  .cta {
    background: red;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
  }

  .cta:hover {
    background: #dc1f1f;
  }

  .hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    width: 24px;
    height: 24px;
    justify-content: center;
  }


.hamburger span {
  display: block;
  height: 3px;
  width: 100%;
  background: #111;
  transition: 0.3s ease;
  border-radius: 2px;
}

  .hero {
    text-align: center;
    padding: 4rem 1rem 2rem;
  }

  .hero h1 {
    font-weight: 900  ;
    font-size: 10rem;
    margin-top: 5rem;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  .hero p {
    margin: 0;
    opacity: 0.75;
  }

  .hero .red {
    color: red;
  }

  .hero-content {
    display: flex;
    flex-direction: column;
    margin-bottom: 2rem;
  }

  .hero .cta {
    margin-top: 4rem;
    margin-bottom: 6rem;
  }

  .screenshot {
    display: flex;
    justify-content: center;
    padding: 2rem;
  }

  .screenshot-img {
    padding: 20px;
  }

  .screenshot img {
    width: 90%;
    max-width: 800px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(44, 44, 87, 0.1);
  }

  .team {
    background: #f1f3f6;
    padding: 3rem 1rem;
    text-align: center;
  }

  .team h2 {
    margin-bottom: 2rem;
  }

  .team-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(180px, 1fr));
    gap: 1.5rem;
    max-width: 960px;
    margin: 0 auto;
  }

  .team-member {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  }

  .avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: #ccc;
    margin: 0 auto 1rem;
    position: relative;
    overflow: hidden;
  }

  .avatar img {
    object-fit: cover;
  }

  .tags span {
    background: #eee;
    font-size: 0.8rem;
    margin: 0.2rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    display: inline-block;
  }

  .email-container {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
    margin-top: 1rem;
  }

  .email-link {
    text-decoration: underline;
    opacity: 0.75;
  }

  .team-email {
    font-size: 0.9rem;
    font-weight: bold;
  }

  .docs {
    padding: 2rem 1rem;
    background: #fff;
  }

  .docs h2 {
    text-align: left;
    max-width: 960px;
    margin: 0 auto 1.5rem;
  }

  .doc-date {
    font-weight: bold;
  }

  .doc-item {
    display: flex;
    justify-content: space-between;
    max-width: 960px;
    margin: 0 auto;
    padding: 1rem;
    background: #f3f4f7;
    border-radius: 8px;
    margin-bottom: 1rem;
  }

  .doc-left {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .download-btn {
    text-decoration: underline;
    opacity: 0.75;
  }

  .cta .arrow {
  margin-left: 0.5rem;
  font-size: 1.1em;
  transition: transform 0.2s ease;
}

.cta:hover .arrow {
  transform: translateX(6px);
}

  /* responsive for tablets / mobile */

@media (max-width: 768px) {
  nav {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    right: 0;
    background: white;
    width: 100vw;
    padding: 0;
    overflow: hidden;
    max-height: 0;
    opacity: 0;
    transition: max-height 0.4s ease, opacity 0.4s ease;
  }

  nav.show {
    max-height: 200px;
    opacity: 1;
    padding: 1rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-top: 1px solid #eee;
  }

  .hamburger {
    display: flex;
  }

  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .team-grid {
    grid-template-columns: 1fr;
  }

  .hero h1 {
    font-size: 4rem;
  }

  .cta {
    width: fit-content;
  }

  .doc-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}


/* animation for hamburger menu */
.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 5px);
}
.hamburger.active span:nth-child(2) {
  opacity: 0;
}
.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -5px);
}

/* animations for logo */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero h1,
.hero p,
.hero .cta {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.hero h1 {
  animation-delay: 0.2s;
}

.hero p {
  animation-delay: 0.6s;
}

.hero .cta {
  animation-delay: 1s;
}
</style>
