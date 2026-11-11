---
# Degree histories index
layout: page
title: "Degree & Order Histories"
lede: "The degrees and orders of the York Rite, and the history behind each."
description: "Histories of the degrees and orders of the York Rite: the four Capitular degrees of the Chapter, the Cryptic degrees of the Council, and the orders of the Knights Templar Commandery."
breadcrumbs:
  - label: "About"
    href: "/about/"
  - label: "Degree Histories"
seo_title: "Degree Histories"
---

Each body of the York Rite confers its own degrees or orders, and each of
them carries a story drawn from the building of Solomon&rsquo;s Temple, its
loss and restoration, and the traditions of medieval chivalry. The pages
below give a short public history of each.

{% for body in site.data.bodies.bodies %}
<h2>{{ body.name }}</h2>
<p>
  {{ body.summary }}
  <a href="{{ body.url }}">About {{ body.short_name }}&nbsp;&rarr;</a>
</p>

<ol class="degree-list">
  {% for degree in body.degrees %}
  <li class="degree-list__item">
    <a class="degree-list__link" href="{{ degree.url }}">{{ degree.name }}</a>
    {% if degree.note %}
      <span class="degree-list__note">{{ degree.note }}</span>
    {% endif %}
  </li>
  {% endfor %}
</ol>
{% endfor %}

{% include keystone-divider.html %}

## A note on these histories

These pages describe the generally documented history of each degree and
order as it is publicly presented in the York Rite. They do not disclose
ritual ceremony, and they do not claim origins that remain matters of
tradition rather than documented fact; where scholars differ, the pages
say so.
