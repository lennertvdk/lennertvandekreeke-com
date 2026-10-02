# Generates the static pages of lennertvandekreeke.com in English, German and Dutch.
# Edit the text here, then run: python3 build.py
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
LANGS = ["en", "de", "nl"]
PREFIX = {"en": "/", "de": "/de/", "nl": "/nl/"}
FORMSPREE = "https://formspree.io/f/mjykqqog"
YOUTUBE = "https://www.youtube.com/channel/UCMHHH4dOREJTJF_ySpgV7mA"
PDF = "/cv/Lebenslauf_Lennert_van_de_Kreeke.pdf"

UI = {
    "en": dict(to_dark="Switch to dark theme", to_light="Switch to light theme", updated="Last updated October 2026",
               langnav="Language", sections="Sections"),
    "de": dict(to_dark="Zum dunklen Design wechseln", to_light="Zum hellen Design wechseln", updated="Zuletzt aktualisiert im Oktober 2026",
               langnav="Sprache", sections="Abschnitte"),
    "nl": dict(to_dark="Overschakelen naar donker thema", to_light="Overschakelen naar licht thema", updated="Laatst bijgewerkt in oktober 2026",
               langnav="Taal", sections="Onderdelen"),
}

TOGGLE_SVG = ('<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7.5" fill="none" '
              'stroke="currentColor" stroke-width="1.5"/><path d="M10 2.5a7.5 7.5 0 0 1 0 15z" fill="currentColor"/></svg>')


def head(lang, title, desc, page, noindex=False):
    alts = "\n".join(f'  <link rel="alternate" hreflang="{l}" href="https://lennertvandekreeke.com{PREFIX[l]}{page}">' for l in LANGS)
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
{alts}
  <link rel="alternate" hreflang="x-default" href="https://lennertvandekreeke.com/{page}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>"""


def lang_switch(lang, page):
    items = []
    for l in LANGS:
        if l == lang:
            items.append(f'<span aria-current="true">{l.upper()}</span>')
        else:
            items.append(f'<a href="{PREFIX[l]}{page}" hreflang="{l}" lang="{l}">{l.upper()}</a>')
    return f'<nav class="lang" aria-label="{UI[lang]["langnav"]}">{"".join(items)}</nav>'


def toggle(lang):
    u = UI[lang]
    return (f'<button class="theme-toggle" type="button" data-to-dark="{u["to_dark"]}" '
            f'data-to-light="{u["to_light"]}" aria-label="{u["to_dark"]}">\n        {TOGGLE_SVG}\n      </button>')


def topbar(lang, page):
    return f"""    <div class="topbar">
      <a class="back" href="{PREFIX[lang]}">&larr; Lennert van de Kreeke</a>
      {lang_switch(lang, page)}
      {toggle(lang)}
    </div>"""


def footer(lang, scripts=("theme.js",)):
    tags = "\n".join(f'  <script src="/{s}"></script>' for s in scripts)
    return f"""  <footer>
    <p>Berlin &middot; {UI[lang]["updated"]}</p>
  </footer>
{tags}
</body>
</html>
"""


def entry(when, body, title=None):
    h = f"\n            <h3>{title}</h3>" if title else ""
    return f"""        <article class="entry">
          <p class="when">{when}</p>
          <div>{h}
            <p>{body}</p>
          </div>
        </article>"""


def section(id_, label, inner):
    return f"""    <section id="{id_}">
      <h2>{label}</h2>
      <div class="body">
{inner}
      </div>
    </section>"""


def a(href, text):
    return f'<a href="{href}">{text}</a>'


# ---------------------------------------------------------------- Home

HOME = {
    "en": dict(
        desc="Final-year medical student at Charité Berlin. Psychedelic research, psychiatry, and organizing things for other students.",
        alt="Lennert smiling down from a stone balustrade, red columns behind him",
        lede="I’m a final-year med student in Berlin. Most of my time goes to the hospital, psychedelic research, and organizing things for other students.",
        toc=["Now", "Research", "Organizing", "Outside medicine", "CV", "Contact"],
        month="October 2026",
        now=["Currently in my Praktisches Jahr: psychiatry, surgery, internal medicine.",
             "Writing up my doctorate for Zurich.",
             "Final exams next summer, then psychiatry."],
        since="Since", ongoing="Ongoing", aug="Aug 2026", also="Also",
        research=[
            ("2024", "Doctorate, University of Zurich",
             "At the Psychiatric University Hospital Zurich, supervised by Milan Scheidegger. I’m looking at what DMT and harmine do to cortisol, prolactin and tryptophan catabolites."),
            ("2026", "EPIsoDE study, Charité",
             "Psilocybin for treatment-resistant depression. I transcribe and analyse recordings of the study visits."),
            (None, "Research assistant, Charité and Zurich",
             "A year working on three clinical studies: EPIsoDE, PRISM (neurofeedback for PTSD) and a 5-MeO-DMT study on embodiment and pain perception."),
        ],
        psng="I started it with two other students in 2025. It now has over 250 members in 13 cities. I look after strategy, money, partnerships and IT, and I rebuilt the website myself. On Instagram as {ig}.",
        bpsa="PSNG’s Berlin group. Talks, community evenings, the website. On Instagram as {ig}.",
        lectures_t="PSNG Lectures",
        lectures="A lecture series we record and put online. I edit the videos and make the thumbnails. So far: Prateep Beed, Eric Lonergan and Torsten Passie. Watch them on {yt}.",
        abend="Our first in-person PSNG × BPSA evening, at the Molecule office in Berlin. A talk, a workshop, an integration talk and a sound meditation. 31 people came and gave it 9/10 on average.",
        alps="Awareness Lectures on Psychedelics in Switzerland. I coordinated the participants for the 2025 edition and ran the whole 2026 one: team, programme, marketing and budget. Now I’m mostly advising.",
        proz="Student group at the University of Zurich and ETH. We ran a lecture series that drew 50 to 100 people and a Swiss student conference.",
        psychag_t="Psych-AG, Charité",
        psychag="The student council’s psychiatry group. Talks, events, and the fundraising to pay for them.",
        photo_alt="Lennert leaning against a stone column in a colonnade",
        bass="Bass guitar, in four bands over eight years, with the odd gig around Berlin.",
        musical="Was in a production of <i>Der kleine Horrorladen</i> (Little Shop of Horrors), and took singing lessons after that.",
        kiezburn="Built a postcard-writing installation at Kiezburn, the Burning Man regional near Berlin. The idea came from Taizé.",
        misc="Running and lifting. Clothes and sneakers, somewhere around Asics × Kiko Kostadinov. Figuring out what makes a gathering actually work. And enough self-taught design to make websites and posters for friends.",
        cv_line="My full CV has its own page: {link}.", cv_link="CV, with a PDF to download",
        contact_intro="The easiest way to reach me is this form. It goes straight to my inbox.",
        f_name="Name", f_email="Email", f_msg="Message", f_send="Send",
        f_sending="Sending…", f_success="Thanks, your message is on its way.",
        f_error="Something went wrong. Please try again in a moment.",
        subject="New message from lennertvandekreeke.com",
        elsewhere="Elsewhere:",
    ),
    "de": dict(
        desc="Medizinstudent im Praktischen Jahr an der Charité Berlin. Psychedelische Forschung, Psychiatrie und Organisieren für andere Studierende.",
        alt="Lennert lächelt von einer Steinbalustrade herab, hinter ihm rote Säulen",
        lede="Ich bin Medizinstudent im letzten Jahr in Berlin. Die meiste Zeit verbringe ich im Krankenhaus, mit psychedelischer Forschung und damit, Dinge für andere Studierende zu organisieren.",
        toc=["Jetzt", "Forschung", "Engagement", "Außerhalb der Medizin", "Lebenslauf", "Kontakt"],
        month="Oktober 2026",
        now=["Gerade im Praktischen Jahr: Psychiatrie, Chirurgie, Innere Medizin.",
             "Ich schreibe meine Doktorarbeit für Zürich.",
             "Nächsten Sommer das Staatsexamen, danach Psychiatrie."],
        since="Seit", ongoing="Laufend", aug="Aug. 2026", also="Außerdem",
        research=[
            ("2024", "Promotion, Universität Zürich",
             "An der Psychiatrischen Universitätsklinik Zürich, betreut von Milan Scheidegger. Ich untersuche, was DMT und Harmin mit Cortisol, Prolaktin und Tryptophan-Kataboliten machen."),
            ("2026", "EPIsoDE-Studie, Charité",
             "Psilocybin bei therapieresistenter Depression. Ich transkribiere die Aufzeichnungen der Studienvisiten und werte sie aus."),
            (None, "Research Assistant, Charité und Zürich",
             "Ein Jahr in drei klinischen Studien: EPIsoDE, PRISM (Neurofeedback bei PTBS) und eine 5-MeO-DMT-Studie zu Embodiment und Schmerzwahrnehmung."),
        ],
        psng="2025 habe ich es mit zwei anderen Studierenden gegründet. Inzwischen sind es über 250 Mitglieder in 13 Städten. Ich kümmere mich um Strategie, Finanzen, Partnerschaften und IT, und die Website habe ich selbst neu gebaut. Auf Instagram als {ig}.",
        bpsa="Die Berliner Gruppe des PSNG. Vorträge, Community-Abende, die Website. Auf Instagram als {ig}.",
        lectures_t="PSNG-Vortragsreihe",
        lectures="Eine Vortragsreihe, die wir aufzeichnen und online stellen. Ich schneide die Videos und gestalte die Thumbnails. Bisher dabei: Prateep Beed, Eric Lonergan und Torsten Passie. Zu sehen auf {yt}.",
        abend="Unser erster PSNG × BPSA-Abend vor Ort, im Büro von Molecule in Berlin. Ein Vortrag, ein Workshop, ein Integrationsgespräch und eine Klangmeditation. 31 Leute kamen und gaben im Schnitt 9/10.",
        alps="Awareness Lectures on Psychedelics in Switzerland. 2025 habe ich die Teilnehmenden koordiniert und 2026 die ganze Ausgabe geleitet: Team, Programm, Marketing und Budget. Inzwischen berate ich vor allem.",
        proz="Studentische Gruppe an der Universität Zürich und der ETH. Wir haben eine Vortragsreihe mit 50 bis 100 Leuten und eine Schweizer Studierendenkonferenz organisiert.",
        psychag_t="Psych-AG, Charité",
        psychag="Die Psychiatrie-AG der Fachschaftsinitiative. Vorträge, Veranstaltungen und das Geld dafür einwerben.",
        photo_alt="Lennert lehnt in einem Säulengang an einer Steinsäule",
        bass="E-Bass, acht Jahre lang in vier Bands, mit gelegentlichen Auftritten in Berlin.",
        musical="Mitgespielt im Musical <i>Der kleine Horrorladen</i>, danach Gesangsunterricht.",
        kiezburn="Bei Kiezburn, dem Burning-Man-Regional bei Berlin, habe ich eine Installation gebaut, an der man Postkarten schreiben konnte. Die Idee kam aus Taizé.",
        misc="Laufen und Krafttraining. Kleidung und Sneaker, irgendwo bei Asics × Kiko Kostadinov. Herausfinden, was ein Treffen wirklich gut macht. Und genug selbst beigebrachtes Design, um Websites und Plakate für Freunde zu machen.",
        cv_line="Mein ausführlicher Lebenslauf hat eine eigene Seite: {link}.", cv_link="Lebenslauf, auch als PDF",
        contact_intro="Am einfachsten erreichst du mich über dieses Formular. Es landet direkt in meinem Postfach.",
        f_name="Name", f_email="E-Mail", f_msg="Nachricht", f_send="Senden",
        f_sending="Wird gesendet…", f_success="Danke, deine Nachricht ist unterwegs.",
        f_error="Da ist etwas schiefgegangen. Bitte versuch es gleich noch einmal.",
        subject="Neue Nachricht über lennertvandekreeke.com",
        elsewhere="Außerdem:",
    ),
    "nl": dict(
        desc="Laatstejaars geneeskundestudent aan de Charité in Berlijn. Psychedelisch onderzoek, psychiatrie en dingen organiseren voor andere studenten.",
        alt="Lennert kijkt glimlachend omlaag vanaf een stenen balustrade, met rode zuilen achter hem",
        lede="Ik ben laatstejaars geneeskundestudent in Berlijn. De meeste tijd gaat naar het ziekenhuis, psychedelisch onderzoek en het organiseren van dingen voor andere studenten.",
        toc=["Nu", "Onderzoek", "Organiseren", "Buiten de geneeskunde", "CV", "Contact"],
        month="oktober 2026",
        now=["Momenteel in mijn praktijkjaar (Praktisches Jahr): psychiatrie, chirurgie, interne geneeskunde.",
             "Ik werk aan mijn promotie voor Zürich.",
             "Volgende zomer mijn artsexamen, daarna psychiatrie."],
        since="Sinds", ongoing="Doorlopend", aug="aug. 2026", also="Verder",
        research=[
            ("2024", "Promotie, Universiteit Zürich",
             "Aan de Psychiatrische Universiteitskliniek Zürich, onder begeleiding van Milan Scheidegger. Ik onderzoek wat DMT en harmine doen met cortisol, prolactine en tryptofaankatabolieten."),
            ("2026", "EPIsoDE-studie, Charité",
             "Psilocybine bij therapieresistente depressie. Ik transcribeer en analyseer opnames van de studiebezoeken."),
            (None, "Onderzoeksassistent, Charité en Zürich",
             "Een jaar werk aan drie klinische studies: EPIsoDE, PRISM (neurofeedback bij PTSS) en een 5-MeO-DMT-studie naar embodiment en pijnwaarneming."),
        ],
        psng="Ik heb het in 2025 met twee andere studenten opgericht. Inmiddels zijn er meer dan 250 leden in 13 steden. Ik zorg voor strategie, financiën, partnerschappen en IT, en ik heb de website zelf opnieuw gebouwd. Op Instagram als {ig}.",
        bpsa="De Berlijnse groep van PSNG. Lezingen, community-avonden, de website. Op Instagram als {ig}.",
        lectures_t="PSNG-lezingen",
        lectures="Een lezingenreeks die we opnemen en online zetten. Ik monteer de video’s en maak de thumbnails. Tot nu toe: Prateep Beed, Eric Lonergan en Torsten Passie. Te zien op {yt}.",
        abend="Onze eerste PSNG × BPSA-avond op locatie, op het kantoor van Molecule in Berlijn. Een lezing, een workshop, een integratiegesprek en een klankmeditatie. Er kwamen 31 mensen, die het gemiddeld een 9/10 gaven.",
        alps="Awareness Lectures on Psychedelics in Switzerland. In 2025 coördineerde ik de deelnemers en in 2026 leidde ik de hele editie: team, programma, marketing en budget. Nu adviseer ik vooral.",
        proz="Studentengroep aan de Universiteit Zürich en de ETH. We organiseerden een lezingenreeks met 50 tot 100 bezoekers en een Zwitserse studentenconferentie.",
        psychag_t="Psych-AG, Charité",
        psychag="De psychiatriewerkgroep van de studentenraad. Lezingen, evenementen en het geld ervoor binnenhalen.",
        photo_alt="Lennert leunt in een zuilengang tegen een stenen zuil",
        bass="Basgitaar, acht jaar lang in vier bands, met af en toe een optreden in Berlijn.",
        musical="Speelde mee in de musical <i>Der kleine Horrorladen</i> (Little Shop of Horrors) en nam daarna zangles.",
        kiezburn="Op Kiezburn, de regionale Burning Man bij Berlijn, bouwde ik een installatie waar je ansichtkaarten kon schrijven. Het idee kwam uit Taizé.",
        misc="Hardlopen en krachttraining. Kleding en sneakers, ergens rond Asics × Kiko Kostadinov. Uitzoeken wat een bijeenkomst echt laat werken. En genoeg zelf aangeleerd design om websites en posters voor vrienden te maken.",
        cv_line="Mijn volledige cv heeft een eigen pagina: {link}.", cv_link="cv, ook als pdf",
        contact_intro="Je bereikt me het makkelijkst via dit formulier. Het komt direct in mijn inbox.",
        f_name="Naam", f_email="E-mail", f_msg="Bericht", f_send="Versturen",
        f_sending="Bezig met versturen…", f_success="Bedankt, je bericht is onderweg.",
        f_error="Er ging iets mis. Probeer het zo nog eens.",
        subject="Nieuw bericht via lennertvandekreeke.com",
        elsewhere="Verder:",
    ),
}


def home(lang, page="", noindex=False):
    t = HOME[lang]
    ids = ["now", "research", "organizing", "outside", "cv", "contact"]
    toc = "\n".join(
        f'        <a href="{PREFIX[lang]}cv/">{label}</a>' if i == "cv" else f'        <a href="#{i}">{label}</a>'
        for i, label in zip(ids, t["toc"]))
    s = t["since"]
    ig = lambda h: a(f"https://www.instagram.com/{h}/", "@" + h)

    now = "\n".join(f"          <li>{x}</li>" for x in t["now"])
    research = "\n".join(entry(f"{s} {y}" if y else "2023", body, title) for y, title, body in t["research"])
    organizing = "\n".join([
        entry(f"{s} 2025", t["psng"].format(ig=ig("psng.info")), a("https://psng.info", "Psychedelic Student Network Germany")),
        entry(f"{s} 2026", t["bpsa"].format(ig=ig("bpsa.berlin")), a("https://bpsa.psng.info", "Berlin Psychedelic Science Association")),
        entry(t["ongoing"], t["lectures"].format(yt=a(YOUTUBE, "YouTube")), a(YOUTUBE, t["lectures_t"])),
        entry(t["aug"], t["abend"], a("https://luma.com/n6io5052", "Ein Abend rund um Psychedelika")),
        entry(f"{s} 2024", t["alps"], a("https://alps.foundation", "ALPS Summer School")),
        entry("2023–2025", t["proz"], a("https://psychedelicresearchzurich.ch", "Psychedelic Research Organization of Zurich")),
        entry("2022–2025", t["psychag"], a("https://fsi-charite.de/ag/psych-ag/", t["psychag_t"])),
    ])
    outside = "\n".join([
        f'        <img class="photo" src="/img/colonnade.jpg" alt="{t["photo_alt"]}" width="1400" height="933" loading="lazy">',
        entry("2014–2022", t["bass"]),
        entry("2022", t["musical"]),
        entry("2026", t["kiezburn"]),
        entry(t["also"], t["misc"]),
    ])
    cv = f'        <p>{t["cv_line"].format(link=a(PREFIX[lang] + "cv/", t["cv_link"]))}</p>'
    contact = f"""        <p>{t["contact_intro"]}</p>
        <form class="contact-form" action="{FORMSPREE}" method="POST" data-sending="{t["f_sending"]}" data-success="{t["f_success"]}" data-error="{t["f_error"]}">
          <input type="hidden" name="_subject" value="{t["subject"]}">
          <input type="hidden" name="language" value="{lang}">
          <label class="hp" aria-hidden="true">Leave empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
          <label>{t["f_name"]} <input type="text" name="name" autocomplete="name" required></label>
          <label>{t["f_email"]} <input type="email" name="email" autocomplete="email" required></label>
          <label>{t["f_msg"]} <textarea name="message" rows="6" required></textarea></label>
          <button class="button" type="submit">{t["f_send"]}</button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
        <p class="elsewhere">{t["elsewhere"]} {a("https://www.instagram.com/l_vd_k/", "Instagram")} &middot; {a("https://www.linkedin.com/in/lennert-van-de-kreeke/", "LinkedIn")} &middot; {a("https://orcid.org/0009-0000-3939-5247", "ORCID")}</p>"""

    body = "\n\n".join([
        section("now", t["toc"][0], f'        <p class="meta">{t["month"]}</p>\n        <ul class="plain">\n{now}\n        </ul>'),
        section("research", t["toc"][1], research),
        section("organizing", t["toc"][2], organizing),
        section("outside", t["toc"][3], outside),
        section("cv", t["toc"][4], cv),
        section("contact", t["toc"][5], contact),
    ])
    return f"""{head(lang, "Lennert van de Kreeke", t["desc"], page, noindex)}
<body>
  <header class="hero">
    <img class="hero-img" src="/img/hero.jpg" srcset="/img/hero-1200.jpg 1200w, /img/hero.jpg 2400w" sizes="100vw" alt="{t["alt"]}" width="2400" height="1600">
    <div class="hero-bar">
      {lang_switch(lang, page)}
      {toggle(lang)}
    </div>
    <div class="hero-text">
      <h1>Lennert van de Kreeke</h1>
      <p class="lede">{t["lede"]}</p>
      <nav class="toc" aria-label="{UI[lang]["sections"]}">
{toc}
      </nav>
    </div>
  </header>

  <main>

{body}

  </main>

{footer(lang, ("theme.js", "contact.js"))}"""


# ---------------------------------------------------------------- CV
# Follows the order and wording of Lebenslauf_van_de_Kreeke.docx. Personal
# contact details (address, phone, email, date of birth) are left out on purpose.

CV = {
    "de": dict(
        title="Lebenslauf", desc="Lebenslauf von Lennert van de Kreeke.",
        intro="Die ausführliche Version, auch zum Herunterladen.", download="Als PDF herunterladen",
        sections=[
            ("Praktisches Jahr", [
                ("05/2026 – 09/2026", "<strong>Psychiatrie und Psychotherapie</strong> · Alexianer St. Hedwig Krankenhaus, Berlin",
                 "<em>Station 37, eine Woche Station 61</em><br>U. a. Aufnahmen mit psychopathologischem Befund sowie körperlicher und neurologischer Untersuchung. Eigenständige Visiten, Angehörigengespräche, Arztbriefe. Blutentnahmen und Zugänge, Anträge, Dokumentation in ORBIS"),
                ("09/2026 – 12/2026", "<strong>Chirurgie</strong> · Evangelische Elisabeth Klinik Berlin (laufend)", None),
                ("12/2026 – 04/2027", "<strong>Innere Medizin</strong> · Jüdisches Krankenhaus Berlin (geplant)", None),
            ]),
            ("Studium und ärztliche Prüfungen", [
                ("seit 10/2019", "<strong>Modellstudiengang Medizin</strong> · Charité – Universitätsmedizin Berlin", None),
                ("09/2023 – 04/2025", "<strong>Auslandsstudium Medizin</strong> · Universität Zürich (SEMP / Erasmus)", "Erstes Masterjahr, anschließend ein Semester für die Promotion"),
                ("Sommer 2027", "<strong>Dritter Abschnitt der Ärztlichen Prüfung und Approbation</strong> · voraussichtlich", None),
                ("04/2026", "<strong>Zweiter Abschnitt der Ärztlichen Prüfung</strong> · befriedigend (74,8 %)", None),
                ("08/2022", "<strong>Erster Abschnitt der Ärztlichen Prüfung</strong> (gleichwertig) · gut (2,0)", None),
            ]),
            ("Famulaturen und Praktika", [
                ("06/2024 – 07/2024", "<strong>Famulatur Psychiatrie</strong> · Psychiatrische Universitätsklinik Zürich, Akutpsychiatrie", "Anamnesen, körperliche und neurologische Untersuchung, Dokumentation, Teilnahme an Visiten"),
                ("02/2024 – 04/2024", "<strong>Famulatur Allgemeinmedizin</strong> · Praxis Dr. med. Udo Werner, Zürich", None),
                ("04/2022", "<strong>Famulatur Kinderonkologie</strong> · Helios Klinikum Berlin-Buch", None),
                ("09/2021 – 10/2021", "<strong>Famulatur Allgemeinmedizin</strong> · Praxis Dr. med. Dirk Laudahn, Berlin", None),
                ("03/2021 – 04/2021", "<strong>Pflegepraktikum Psychiatrie</strong> · Vivantes Humboldt-Klinikum, Berlin", "Pflegerische Aufgaben in Akutpsychiatrie und Suchtmedizin"),
            ]),
            ("Engagement und Lehre", [
                ("seit 04/2025", "<strong>Psychedelic Student Network Germany</strong> · Mitgründer",
                 "<em>Bundesweites studentisches Netzwerk, über 250 Mitglieder in 13 Städten, {psng}</em><br>2025 initiiert und mit zwei weiteren Studierenden gegründet. Verantwortung für Strategie, Finanzen, Partnerschaften, Marketing, Mitgliedergewinnung und IT, Eventorganisation und Aufbau einer Vortragsreihe"),
                ("seit 2026", "<strong>Berlin Psychedelic Science Association</strong> · Mitorganisator",
                 "<em>Berliner Lokalgruppe des PSNG, {bpsa}</em><br>Vortrags- und Community-Veranstaltungen, Website und Marketing"),
                ("seit 10/2024", "<strong>ALPS Summer School</strong> · Mitorganisator",
                 "<em>Awareness Lectures on Psychedelics in Switzerland, {alps}</em><br>Gesamtkoordination der Ausgabe 2026: Team, Programm, Marketing und rund 35.000 Euro Budget, seit 03/2026 beratend. Zuvor Teilnehmendenkoordination der Ausgabe 2025"),
                ("10/2023 – 03/2025", "<strong>Psychedelic Research Organization of Zurich</strong> · Mitorganisator",
                 "<em>Studentische Organisation an Universität und ETH Zürich</em><br>Vortragsreihe mit 50 bis 100 Teilnehmenden, Schweizer Studierendenkonferenz"),
                ("04/2022 – 12/2025", "<strong>Psych-AG</strong> · Mitorganisator",
                 "<em>Fachschaftsinitiative (FSI) der Charité</em><br>Fachvorträge und Eventorganisation, Mitteleinwerbung über die FSI"),
                ("2021 – 2024", "<strong>Nachhilfe und Peer-Mentoring</strong>",
                 "Nachhilfe in Mathematik, Deutsch und Chemie<br>Peer-Mentoring-Programm der Charité für Erstsemesterstudierende"),
            ]),
            ("Promotion und Wissenschaft", [
                ("seit 01/2024", "<strong>Promotion</strong> · Universität Zürich, Psychiatrische Universitätsklinik",
                 "Cortisol, Prolaktin und Tryptophan-Katabolite unter DMT- und Harmin-Gabe<br>Betreuung: PD Dr. med. Milan Scheidegger"),
                ("seit 08/2026", "<strong>EPIsoDE-Studie</strong> · Research Assistant, Charité",
                 "Psilocybin bei therapieresistenter Depression, Transkription und Auswertung von Visitenaufzeichnungen"),
                ("03/2023 – 12/2023", "<strong>Klinische Studien</strong> · Research Assistant, Charité und Universität Zürich",
                 "EPIsoDE: Psilocybin bei therapieresistenter Depression, Charité<br>PRISM: Neurofeedback bei posttraumatischer Belastungsstörung, Charité<br>5-MeO-DMT: Embodiment und Schmerzwahrnehmung, Zürich<br>Studiendurchführung und Datenerhebung in Voll- und Teilzeit"),
            ]),
            ("Fortbildungen und Kongresse", [
                ("09/2025", "<strong>Autumn School Psychopharmakologie</strong> · DGPPN", "Leitung: Prof. Dr. med. Gerhard Gründer"),
                ("07/2025", "<strong>Summer School on Psychedelic Research</strong> · University of Groningen", None),
                ("2023 – 2026", "<strong>Kongresse</strong> · DGPPN, ALPS Conference (auch im Team), SÄPT, ICPR, INSIGHT", None),
            ]),
            ("Berufserfahrung", [
                ("01/2021 – 12/2021", "<strong>InVitro Diagnostik Lorenz</strong> · Labormitarbeiter, Berlin", "SARS-CoV-2-Diagnostik und Aufgaben der Schichtleitung"),
            ]),
            ("Sprachen und Kenntnisse", [
                ("Sprachen", "Deutsch und Niederländisch (Muttersprachen), Englisch (verhandlungssicher, C1), Französisch (Grundkenntnisse, B1)", None),
                ("EDV", "ORBIS, Office-Anwendungen, R", None),
            ]),
            ("Interessen", [
                ("Musik und Sport", "E-Bass seit 2014, acht Jahre in vier Bands mit gelegentlichen Auftritten in Berlin",
                 "Musical „Der kleine Horrorladen“ (2022), anschließend Gesangsausbildung<br>Ausdauer- und Kraftsport"),
            ]),
        ],
    ),
    "en": dict(
        title="CV", desc="CV of Lennert van de Kreeke.",
        intro="The full version. There’s also a PDF, in German.", download="Download PDF (German)",
        sections=[
            ("Praktisches Jahr (final-year rotations)", [
                ("05/2026 – 09/2026", "<strong>Psychiatry and psychotherapy</strong> · Alexianer St. Hedwig Krankenhaus, Berlin",
                 "<em>Ward 37, one week on ward 61</em><br>Among other things: admissions with psychopathological, physical and neurological examination. Ward rounds on my own, talks with relatives, discharge letters. Blood draws and IV lines, applications, documentation in ORBIS"),
                ("09/2026 – 12/2026", "<strong>Surgery</strong> · Evangelische Elisabeth Klinik Berlin (ongoing)", None),
                ("12/2026 – 04/2027", "<strong>Internal medicine</strong> · Jüdisches Krankenhaus Berlin (planned)", None),
            ]),
            ("Medical school and state exams", [
                ("since 10/2019", "<strong>Medicine (Modellstudiengang)</strong> · Charité – Universitätsmedizin Berlin", None),
                ("09/2023 – 04/2025", "<strong>Study abroad</strong> · University of Zurich (SEMP / Erasmus)", "First master’s year, then one semester for the doctorate"),
                ("Summer 2027", "<strong>Third state exam and medical licence</strong> · expected", None),
                ("04/2026", "<strong>Second state exam</strong> · satisfactory (74.8 %)", None),
                ("08/2022", "<strong>First state exam</strong> (equivalent) · good (2.0)", None),
            ]),
            ("Clinical placements", [
                ("06/2024 – 07/2024", "<strong>Clerkship in psychiatry</strong> · Psychiatric University Hospital Zurich, acute psychiatry", "History taking, physical and neurological examination, documentation, ward rounds"),
                ("02/2024 – 04/2024", "<strong>Clerkship in general practice</strong> · Practice of Dr. med. Udo Werner, Zurich", None),
                ("04/2022", "<strong>Clerkship in paediatric oncology</strong> · Helios Klinikum Berlin-Buch", None),
                ("09/2021 – 10/2021", "<strong>Clerkship in general practice</strong> · Practice of Dr. med. Dirk Laudahn, Berlin", None),
                ("03/2021 – 04/2021", "<strong>Nursing placement in psychiatry</strong> · Vivantes Humboldt-Klinikum, Berlin", "Nursing duties in acute psychiatry and addiction medicine"),
            ]),
            ("Organizing and teaching", [
                ("since 04/2025", "<strong>Psychedelic Student Network Germany</strong> · Co-founder",
                 "<em>Nationwide student network, over 250 members in 13 cities, {psng}</em><br>Started it in 2025 and founded it with two other students. Responsible for strategy, finances, partnerships, marketing, member recruitment and IT, event organization and building a lecture series"),
                ("since 2026", "<strong>Berlin Psychedelic Science Association</strong> · Co-organizer",
                 "<em>PSNG’s Berlin group, {bpsa}</em><br>Talks and community events, website and marketing"),
                ("since 10/2024", "<strong>ALPS Summer School</strong> · Co-organizer",
                 "<em>Awareness Lectures on Psychedelics in Switzerland, {alps}</em><br>Overall coordination of the 2026 edition: team, programme, marketing and a budget of around €35,000; advisory role since 03/2026. Before that, participant coordination for the 2025 edition"),
                ("10/2023 – 03/2025", "<strong>Psychedelic Research Organization of Zurich</strong> · Co-organizer",
                 "<em>Student organization at the University of Zurich and ETH Zurich</em><br>Lecture series with 50 to 100 attendees, Swiss student conference"),
                ("04/2022 – 12/2025", "<strong>Psych-AG</strong> · Co-organizer",
                 "<em>Student council initiative (FSI) at Charité</em><br>Talks and events, fundraising through the FSI"),
                ("2021 – 2024", "<strong>Tutoring and peer mentoring</strong>",
                 "Tutoring in maths, German and chemistry<br>Charité peer mentoring programme for first-year students"),
            ]),
            ("Doctorate and research", [
                ("since 01/2024", "<strong>Doctorate</strong> · University of Zurich, Psychiatric University Hospital",
                 "Cortisol, prolactin and tryptophan catabolites after DMT and harmine administration<br>Supervisor: PD Dr. med. Milan Scheidegger"),
                ("since 08/2026", "<strong>EPIsoDE study</strong> · Research assistant, Charité",
                 "Psilocybin for treatment-resistant depression; transcription and analysis of visit recordings"),
                ("03/2023 – 12/2023", "<strong>Clinical studies</strong> · Research assistant, Charité and University of Zurich",
                 "EPIsoDE: psilocybin for treatment-resistant depression, Charité<br>PRISM: neurofeedback for post-traumatic stress disorder, Charité<br>5-MeO-DMT: embodiment and pain perception, Zurich<br>Running studies and collecting data, full- and part-time"),
            ]),
            ("Courses and conferences", [
                ("09/2025", "<strong>Autumn School in Psychopharmacology</strong> · DGPPN", "Led by Prof. Dr. med. Gerhard Gründer"),
                ("07/2025", "<strong>Summer School on Psychedelic Research</strong> · University of Groningen", None),
                ("2023 – 2026", "<strong>Conferences</strong> · DGPPN, ALPS Conference (also on the team), SÄPT, ICPR, INSIGHT", None),
            ]),
            ("Work experience", [
                ("01/2021 – 12/2021", "<strong>InVitro Diagnostik Lorenz</strong> · Lab technician, Berlin", "SARS-CoV-2 testing and shift lead duties"),
            ]),
            ("Languages and skills", [
                ("Languages", "German and Dutch (native), English (fluent, C1), French (basic, B1)", None),
                ("Software", "ORBIS, Office, R", None),
            ]),
            ("Interests", [
                ("Music and sport", "Bass guitar since 2014, eight years in four bands with occasional gigs in Berlin",
                 "The musical <i>Der kleine Horrorladen</i> (2022), then singing lessons<br>Endurance and strength training"),
            ]),
        ],
    ),
    "nl": dict(
        title="CV", desc="Cv van Lennert van de Kreeke.",
        intro="De volledige versie. Er is ook een pdf, in het Duits.", download="Download als pdf (Duits)",
        sections=[
            ("Praktijkjaar (Praktisches Jahr)", [
                ("05/2026 – 09/2026", "<strong>Psychiatrie en psychotherapie</strong> · Alexianer St. Hedwig Krankenhaus, Berlijn",
                 "<em>Afdeling 37, een week op afdeling 61</em><br>Onder andere opnames met psychopathologisch, lichamelijk en neurologisch onderzoek. Zelfstandig visites lopen, gesprekken met naasten, ontslagbrieven. Bloedafnames en infusen, aanvragen, documentatie in ORBIS"),
                ("09/2026 – 12/2026", "<strong>Chirurgie</strong> · Evangelische Elisabeth Klinik Berlin (lopend)", None),
                ("12/2026 – 04/2027", "<strong>Interne geneeskunde</strong> · Jüdisches Krankenhaus Berlin (gepland)", None),
            ]),
            ("Studie en artsexamens", [
                ("sinds 10/2019", "<strong>Geneeskunde (Modellstudiengang)</strong> · Charité – Universitätsmedizin Berlin", None),
                ("09/2023 – 04/2025", "<strong>Studie in het buitenland</strong> · Universiteit Zürich (SEMP / Erasmus)", "Eerste masterjaar, daarna een semester voor de promotie"),
                ("Zomer 2027", "<strong>Derde deel van het artsexamen en artsbevoegdheid</strong> · verwacht", None),
                ("04/2026", "<strong>Tweede deel van het artsexamen</strong> · voldoende (74,8 %)", None),
                ("08/2022", "<strong>Eerste deel van het artsexamen</strong> (gelijkwaardig) · goed (2,0)", None),
            ]),
            ("Stages", [
                ("06/2024 – 07/2024", "<strong>Stage psychiatrie</strong> · Psychiatrische Universiteitskliniek Zürich, acute psychiatrie", "Anamneses, lichamelijk en neurologisch onderzoek, documentatie, deelname aan visites"),
                ("02/2024 – 04/2024", "<strong>Stage huisartsgeneeskunde</strong> · Praktijk Dr. med. Udo Werner, Zürich", None),
                ("04/2022", "<strong>Stage kinderoncologie</strong> · Helios Klinikum Berlin-Buch", None),
                ("09/2021 – 10/2021", "<strong>Stage huisartsgeneeskunde</strong> · Praktijk Dr. med. Dirk Laudahn, Berlijn", None),
                ("03/2021 – 04/2021", "<strong>Verpleegstage psychiatrie</strong> · Vivantes Humboldt-Klinikum, Berlijn", "Verpleegkundige taken in acute psychiatrie en verslavingszorg"),
            ]),
            ("Organiseren en onderwijs", [
                ("sinds 04/2025", "<strong>Psychedelic Student Network Germany</strong> · Medeoprichter",
                 "<em>Landelijk studentennetwerk, meer dan 250 leden in 13 steden, {psng}</em><br>In 2025 opgezet en met twee andere studenten opgericht. Verantwoordelijk voor strategie, financiën, partnerschappen, marketing, ledenwerving en IT, evenementen en het opzetten van een lezingenreeks"),
                ("sinds 2026", "<strong>Berlin Psychedelic Science Association</strong> · Mede-organisator",
                 "<em>De Berlijnse groep van PSNG, {bpsa}</em><br>Lezingen en community-evenementen, website en marketing"),
                ("sinds 10/2024", "<strong>ALPS Summer School</strong> · Mede-organisator",
                 "<em>Awareness Lectures on Psychedelics in Switzerland, {alps}</em><br>Algehele coördinatie van de editie 2026: team, programma, marketing en een budget van ongeveer € 35.000, sinds 03/2026 als adviseur. Daarvoor coördinatie van de deelnemers voor de editie 2025"),
                ("10/2023 – 03/2025", "<strong>Psychedelic Research Organization of Zurich</strong> · Mede-organisator",
                 "<em>Studentenorganisatie aan de Universiteit Zürich en de ETH Zürich</em><br>Lezingenreeks met 50 tot 100 bezoekers, Zwitserse studentenconferentie"),
                ("04/2022 – 12/2025", "<strong>Psych-AG</strong> · Mede-organisator",
                 "<em>Initiatief van de studentenraad (FSI) van de Charité</em><br>Vakinhoudelijke lezingen en evenementen, fondsenwerving via de FSI"),
                ("2021 – 2024", "<strong>Bijles en peer-mentoring</strong>",
                 "Bijles wiskunde, Duits en scheikunde<br>Peer-mentoringprogramma van de Charité voor eerstejaars"),
            ]),
            ("Promotie en onderzoek", [
                ("sinds 01/2024", "<strong>Promotie</strong> · Universiteit Zürich, Psychiatrische Universiteitskliniek",
                 "Cortisol, prolactine en tryptofaankatabolieten na toediening van DMT en harmine<br>Begeleiding: PD Dr. med. Milan Scheidegger"),
                ("sinds 08/2026", "<strong>EPIsoDE-studie</strong> · Onderzoeksassistent, Charité",
                 "Psilocybine bij therapieresistente depressie, transcriptie en analyse van opnames van studiebezoeken"),
                ("03/2023 – 12/2023", "<strong>Klinische studies</strong> · Onderzoeksassistent, Charité en Universiteit Zürich",
                 "EPIsoDE: psilocybine bij therapieresistente depressie, Charité<br>PRISM: neurofeedback bij posttraumatische stressstoornis, Charité<br>5-MeO-DMT: embodiment en pijnwaarneming, Zürich<br>Uitvoering van studies en dataverzameling, voltijd en deeltijd"),
            ]),
            ("Cursussen en congressen", [
                ("09/2025", "<strong>Autumn School Psychofarmacologie</strong> · DGPPN", "Onder leiding van Prof. Dr. med. Gerhard Gründer"),
                ("07/2025", "<strong>Summer School on Psychedelic Research</strong> · Rijksuniversiteit Groningen", None),
                ("2023 – 2026", "<strong>Congressen</strong> · DGPPN, ALPS Conference (ook in het team), SÄPT, ICPR, INSIGHT", None),
            ]),
            ("Werkervaring", [
                ("01/2021 – 12/2021", "<strong>InVitro Diagnostik Lorenz</strong> · Laboratoriummedewerker, Berlijn", "SARS-CoV-2-diagnostiek en taken als ploegleider"),
            ]),
            ("Talen en vaardigheden", [
                ("Talen", "Duits en Nederlands (moedertalen), Engels (vloeiend, C1), Frans (basiskennis, B1)", None),
                ("Software", "ORBIS, Office, R", None),
            ]),
            ("Interesses", [
                ("Muziek en sport", "Basgitaar sinds 2014, acht jaar in vier bands met af en toe een optreden in Berlijn",
                 "De musical <i>Der kleine Horrorladen</i> (2022), daarna zangles<br>Duur- en krachtsport"),
            ]),
        ],
    ),
}

CV_LINKS = dict(psng=a("https://psng.info", "psng.info"), bpsa=a("https://bpsa.psng.info", "bpsa.psng.info"),
                alps=a("https://alps.foundation", "alps.foundation"))


def cv(lang):
    t = CV[lang]
    parts = []
    for label, rows in t["sections"]:
        entries = []
        for when, main, extra in rows:
            x = f"\n            <p>{extra.format(**CV_LINKS)}</p>" if extra else ""
            entries.append(f"""        <article class="entry">
          <p class="when">{when}</p>
          <div>
            <p>{main}</p>{x}
          </div>
        </article>""")
        parts.append(section(label.lower().split(" ")[0].replace("ä", "ae"), label, "\n".join(entries)))
    return f"""{head(lang, f"{t['title']} · Lennert van de Kreeke", t["desc"], "cv/")}
<body class="cv-page">
  <main>

{topbar(lang, "cv/")}

    <header class="page-head">
      <h1>{t["title"]}</h1>
      <p class="lede">{t["intro"]}</p>
      <a class="button" href="{PDF}" download>{t["download"]}</a>
    </header>

{chr(10).join(parts)}

  </main>

{footer(lang)}"""


# ---------------------------------------------------------------- Websites (unlinked)

SITES = {
    "en": dict(title="Websites", progress="In progress",
               lede="Sites I’ve built, mostly for groups I’m part of and for friends. I taught myself as I went.",
               psng="The website for PSNG, in German and English. Events, the team, an FAQ and a guide for starting a group in your own city. It replaced our old Google Sites page.",
               bpsa="A small site for our Berlin group. It mainly shows the next talk and gets people into the WhatsApp group.",
               lustig="A joke site for a friend who plays the organ. It’s meant to be terrible. Turn the music on.",
               niklas="A portfolio for the same friend, who’s a conductor and organist in Berlin. Bio, repertoire, dates, recordings and press.",
               biblio="A site for a library association in Solothurn that collects and preserves books on psychedelics and altered states.",
               shot="Homepage of"),
    "de": dict(title="Websites", progress="In Arbeit",
               lede="Websites, die ich gebaut habe, meist für Gruppen, in denen ich aktiv bin, und für Freunde. Beigebracht habe ich mir das nebenbei selbst.",
               psng="Die Website des PSNG, auf Deutsch und Englisch. Veranstaltungen, das Team, ein FAQ und ein Leitfaden, um in der eigenen Stadt eine Gruppe zu gründen. Sie hat unsere alte Google-Sites-Seite ersetzt.",
               bpsa="Eine kleine Seite für unsere Berliner Gruppe. Sie zeigt vor allem den nächsten Vortrag und bringt Leute in die WhatsApp-Gruppe.",
               lustig="Eine Spaßseite für einen Freund, der Orgel spielt. Sie soll schlimm sein. Musik anmachen.",
               niklas="Ein Portfolio für denselben Freund, Dirigent und Organist in Berlin. Vita, Repertoire, Termine, Aufnahmen und Presse.",
               biblio="Eine Website für einen Bibliotheksverein in Solothurn, der Bücher über Psychedelika und veränderte Bewusstseinszustände sammelt und bewahrt.",
               shot="Startseite von"),
    "nl": dict(title="Websites", progress="In de maak",
               lede="Websites die ik heb gebouwd, vooral voor groepen waar ik bij betrokken ben en voor vrienden. Ik heb het mezelf al doende geleerd.",
               psng="De website van PSNG, in het Duits en Engels. Evenementen, het team, een FAQ en een handleiding om in je eigen stad een groep te beginnen. Hij verving onze oude Google Sites-pagina.",
               bpsa="Een kleine site voor onze Berlijnse groep. Hij laat vooral de volgende lezing zien en brengt mensen naar de WhatsApp-groep.",
               lustig="Een grapsite voor een vriend die orgel speelt. Hij hoort verschrikkelijk te zijn. Zet de muziek aan.",
               niklas="Een portfolio voor dezelfde vriend, dirigent en organist in Berlijn. Bio, repertoire, data, opnames en pers.",
               biblio="Een site voor een bibliotheekvereniging in Solothurn die boeken over psychedelica en veranderde bewustzijnstoestanden verzamelt en bewaart.",
               shot="Homepage van"),
}


def site(t, domain, shot, name, text, stack=None, progress=False, first=False):
    lazy = "" if first else ' loading="lazy"'
    tag = f' <span class="tag">{t["progress"]}</span>' if progress else ""
    st = f'\n          <p class="stack">{stack}</p>' if stack else ""
    url = f"https://{domain}"
    return f"""      <article class="site">
        <a class="frame" href="{url}">
          <div class="bar">{domain}</div>
          <img src="/websites/shots/{shot}.jpg" alt="{t["shot"]} {domain}"{lazy} width="1440" height="900">
        </a>
        <div class="site-text">
          <h2><a href="{url}">{name}</a>{tag}</h2>
          <p>{text}</p>{st}
        </div>
      </article>"""


def websites(lang):
    t = SITES[lang]
    items = "\n\n".join([
        site(t, "psng.info", "psng", "Psychedelic Student Network Germany", t["psng"], "React · Vite · Tailwind", first=True),
        site(t, "bpsa.psng.info", "bpsa", "Berlin Psychedelic Science Association", t["bpsa"]),
        site(t, "unlustig.niklaslustig.de", "unlustig", "Lustig Lustig", t["lustig"]),
        site(t, "niklaslustig.de", "niklaslustig", "Niklas Lustig", t["niklas"], "Astro", progress=True),
        site(t, "bibliotheca.psychedelicscience.eu", "bibliotheca", "Bibliotheca Psychonautica", t["biblio"], progress=True),
    ])
    return f"""{head(lang, f"{t['title']} · Lennert van de Kreeke", t["lede"], "websites/", noindex=True)}
<body class="wide">
  <main>

{topbar(lang, "websites/")}

    <header class="page-head">
      <h1>{t["title"]}</h1>
      <p class="lede">{t["lede"]}</p>
    </header>

    <div class="sites">

{items}

    </div>

  </main>

{footer(lang)}"""


# ---------------------------------------------------------------- 404 (one page, all three languages)

NOTFOUND = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found · Lennert van de Kreeke</title>
  <meta name="robots" content="noindex">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
  <main>

    <div class="topbar">
      <a class="back" href="/">&larr; Lennert van de Kreeke</a>
      {toggle("en")}
    </div>

    <header class="page-head notfound">
      <h1>404</h1>
      <p class="lede">This page doesn’t exist. <a href="/">Back to the homepage</a>.</p>
      <p class="lede" lang="de">Diese Seite gibt es nicht. <a href="/de/">Zurück zur Startseite</a>.</p>
      <p class="lede" lang="nl">Deze pagina bestaat niet. <a href="/nl/">Terug naar de homepage</a>.</p>
    </header>

  </main>

{footer("en")}"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


for lang in LANGS:
    p = "" if lang == "en" else f"{lang}/"
    write(f"{p}index.html", home(lang))
    # The original long homepage, kept unlinked for reference.
    write(f"{p}landingpage/index.html", home(lang, "landingpage/", noindex=True))
    write(f"{p}cv/index.html", cv(lang))
    write(f"{p}websites/index.html", websites(lang))
write("404.html", NOTFOUND)
