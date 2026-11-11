---
# Royal Arch Chapter page
layout: body
body_key: chapter
title: "Chapter of Royal Arch Masons"
seo_title: "Royal Arch Chapter"
description: "The Chapter of Royal Arch Masons of Montgomery County, Maryland. Royal Arch Masonry is the first part of the York Rite system of the Masonic degrees, with four conferring degrees."
breadcrumbs:
  - label: "About"
    href: "/about/"
  - label: "Chapter of Royal Arch Masons"
cta:
  title: "Interested in Royal Arch Masonry?"
  text: "If you are a Master Mason in good standing and would like to find out more about the Chapter, please get in touch."
---

Royal Arch Masonry is the first part of the York Rite system of the Masonic
degrees.

## Degrees of the Chapter

Royal Arch Masons meet as a Chapter, and the Royal Arch Chapter confers four
degrees, each with its own history:

{% assign body_data = site.data.bodies.bodies | where: "key", page.body_key | first %}
{% assign body_degrees = body_data.degrees %}

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

A fuller account of each degree is on its history page, and the four are
indexed together on the [degree histories](/about/degrees/) page.

## Historical background

After the independence of the American Colonies in 1776, Freemasonry in the
United States remained relatively little influenced by the rivalry between the
&ldquo;Antients&rdquo; and &ldquo;Moderns&rdquo; in England. In 1797, a group
of Royal Arch masons met in Hartford to try to establish some sort of governing
body for degrees that were largely conferred in the New England states, which
became the Grand Chapter of the Northern States, and later was broken down into
the state-by-state Grand Chapter system. This body later became the General
Grand Chapter, Royal Arch Masons International.

On 10 November 2004, the Grand Chapter of the Holy Royal Arch in England
declared the Royal Arch to be a separate degree in its own right, albeit the
natural progression from the third degree, and the completion of
&ldquo;pure, antient Masonry&rdquo;, which consists of the three Craft degrees
and the Royal Arch.

Following this decision by the Grand Chapter in 2004, there are currently
significant ritual differences between Royal Arch Masonry as worked in England
and Royal Arch Masonry worked as part of the York Rite in the USA. Fraternal
inter-relations remain as before.

## Continuing the journey

The Chapter is the first part of the York Rite. The
[Council of Cryptic Masons](/about/council/) and the
[Commandery of Knights Templar](/about/commandery/) complete the progression.
