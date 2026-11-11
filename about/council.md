---
# Cryptic Council page
layout: body
body_key: council
title: "Council of Cryptic Masons"
seo_title: "Cryptic Council"
description: "The Council of Cryptic Masons of Montgomery County, Maryland. Cryptic Masonry is the second part of the York Rite system of Masonic degrees, and the last found within the Rite that deals specifically with the Hiramic Legend."
breadcrumbs:
  - label: "About"
    href: "/about/"
  - label: "Council of Cryptic Masons"
cta:
  title: "Interested in Cryptic Masonry?"
  text: "If you are a Royal Arch Mason and would like to find out more about the Council, please get in touch."
---

Cryptic Masonry is the second part of the York Rite system of Masonic degrees,
and the last found within the Rite that deals specifically with the Hiramic
Legend.

{% assign body_data = site.data.bodies.bodies | where: "key", page.body_key | first %}
{% assign body_degrees = body_data.degrees %}

## Degrees of the Council

The Council confers the two principal Cryptic degrees, and in many
jurisdictions adds an honorary degree as well, each with its own history:

<ol class="degree-list">
  {% for degree in body_degrees %}
  <li class="degree-list__item">
    <a class="degree-list__link" href="{{ degree.url }}">{{ degree.name }}</a>
    {% if degree.note %}
      <span class="degree-list__note">{{ degree.note }}</span>
    {% endif %}
  </li>
  {% endfor %}
</ol>

Their histories are indexed together on the
[degree histories](/about/degrees/) page.

## The role of the Council

These degrees are the gateway to Temple restoration rituals or the Second
Temple Legend. The body itself is known as either the Council of Royal &amp;
Select Masters or Council of Cryptic Masons depending on the jurisdiction.

## Within the Rite

In Montgomery County the Council works alongside the
[Chapter of Royal Arch Masons](/about/chapter/), whose degrees precede it in
the York Rite, and whose members it prepares for the
[orders of the Knights Templar](/about/commandery/).
