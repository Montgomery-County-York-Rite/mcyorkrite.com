---
# Homepage: Montgomery County York Rite
layout: home
title: "Home"
seo_plain: true
seo_title: "York Rite of Montgomery County, Maryland"
description: "The York Rite Bodies of Montgomery County, Maryland: a Chapter of Royal Arch Masons, a Council of Cryptic Masons, and a Commandery of Knights Templar, meeting at Pentalpha Lodge #194, Germantown."

hero:
  eyebrow: "Montgomery County · Maryland"
  title: "Welcome to the York Rite of Montgomery County"
  lede: "A fellowship of Royal Arch, Cryptic, and Templar Masons. The Montgomery County York Rite is a collection of Appendant Bodies that operate independently of each other."
  primary_label: "Discover the York Rite"
  primary_href: "/about/"
  secondary_label: "Contact Us"
  secondary_href: "/contact/"
---

{% include hero.html %}

<section class="intro-band" aria-labelledby="intro-title">
  <div class="container intro-band__inner">
    <div class="intro-band__text">
      <p class="eyebrow">What is the York Rite?</p>
      <h2 class="section-title" id="intro-title">One Rite, three venerable bodies</h2>
      <p>
        The York Rite is one of the systems of Masonic degrees followed in the
        United States. In Montgomery County it is made up of three appendant
        bodies: a <strong>Chapter of Royal Arch Masons</strong>, a
        <strong>Council of Cryptic Masons</strong>, and a
        <strong>Commandery of Knights Templar</strong>, each with its own
        officers, degrees or orders, and traditions.
      </p>
      <p>
        If you are a Master Mason in good standing from a regular Jurisdiction,
        you may be eligible to join.
      </p>
    </div>
    <div class="intro-band__aside">
      <div class="info-card">
        <p class="eyebrow">Stated Meetings</p>
        <ul class="meeting-list">
          {% for meeting in site.data.organization.meetings %}
            <li><span>{{ meeting.day }}</span><span class="meeting-list__time">{{ meeting.time }}</span></li>
          {% endfor %}
        </ul>
        <p class="info-card__foot">{{ site.data.organization.meeting_location.lodge }}, {{ site.data.organization.meeting_location.city }}, Maryland</p>
        <a class="arrow-link" href="/contact/">Meeting location details<span class="visually-hidden">: see the contact page</span></a>
      </div>
    </div>
  </div>
</section>

{% include keystone-divider.html %}

<section class="bodies-section" aria-labelledby="bodies-title">
  <div class="container">
    <header class="section-header">
      <p class="eyebrow">The Three Bodies</p>
      <h2 class="section-title" id="bodies-title">The York Rite progression</h2>
      <p class="section-lede">Each body confers its own degrees or orders and continues the story begun in the Symbolic Lodge.</p>
    </header>

    <div class="body-grid">
      {% for body in site.data.bodies.bodies %}
        {% include body-card.html body = body %}
      {% endfor %}
    </div>
  </div>
</section>

<section class="tradition-section" aria-labelledby="tradition-title">
  <div class="container tradition-section__inner">
    <div class="tradition-section__text">
      <p class="eyebrow">Tradition &amp; Fellowship</p>
      <h2 class="section-title" id="tradition-title">Rooted in heritage, alive in fellowship</h2>
      <p>
        The York Rite takes its name from the English city of York, long
        associated in Masonic tradition with the early history of the Craft.
        Its degrees and orders draw on the building of King Solomon&rsquo;s
        Temple, its destruction, and its rebuilding, and on the traditions of
        the medieval Knights Templar.
      </p>
      <p>
        In Montgomery County, the three bodies meet together at Pentalpha
        Lodge #194 in Germantown, sharing in ritual, fellowship, and support
        for their communities.
      </p>
      <a class="arrow-link" href="/about/">Read more about the York Rite<span class="visually-hidden">: on the About page</span></a>
    </div>
    <div class="tradition-section__art" aria-hidden="true">
      <svg viewBox="0 0 320 300" focusable="false">
        <g fill="none" stroke="#BA9555" stroke-width="2">
          <path d="M60 280 V 120 A 100 100 0 0 1 260 120 V 280"/>
          <path d="M84 280 V 128 A 76 76 0 0 1 236 128 V 280"/>
          <path d="M146 56 L174 56 L166 90 L154 90 Z" fill="#BA9555" fill-opacity="0.22"/>
          <path d="M146 56 L174 56 L166 90 L154 90 Z"/>
          <path d="M40 280 H 280"/>
          <path d="M40 292 H 280" stroke-opacity="0.5"/>
        </g>
      </svg>
    </div>
  </div>
</section>

<section class="events-section" aria-labelledby="events-title">
  <div class="container events-section__inner">
    <div class="events-section__text">
      <p class="eyebrow">Meetings &amp; Events</p>
      <h2 class="section-title" id="events-title">Come and see</h2>
      <p>
        The bodies meet at {{ site.data.organization.meeting_location.lodge }} in
        {{ site.data.organization.meeting_location.city }}. Upcoming degrees,
        festivals, and community events are kept on our public calendar.
      </p>
    </div>
    <div class="events-section__actions">
      <a class="btn btn--primary" href="/events/">View the Calendar</a>
    </div>
  </div>
</section>

<section class="cta-band" aria-labelledby="cta-title">
  <div class="container cta-band__inner">
    <div class="cta-band__text">
      <h2 class="cta-band__title" id="cta-title">Get involved</h2>
      <p class="cta-band__text-lede">
        If you want to find out more about the York Rite and its associated
        appendant bodies, please don&rsquo;t hesitate to contact us.
      </p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--gold" href="/contact/">Contact Us</a>
      <a class="btn btn--outline-light" href="mailto:{{ site.data.organization.email }}">Email us</a>
    </div>
  </div>
</section>
