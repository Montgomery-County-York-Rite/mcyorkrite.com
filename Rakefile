# Common development tasks for mcyorkrite.com.
# Usage: bundle exec rake -T

require "pathname"

SITE = Pathname.new(__dir__)

desc "Build the site into _site (production settings)"
task :build do
  sh "bundle exec jekyll build --strict_front_matter --trace"
end

desc "Serve the site locally at http://127.0.0.1:4000"
task :serve do
  sh "bundle exec jekyll serve --strict_front_matter"
end

desc "Validate the generated _site output"
task :validate do
  sh "python3 tests/validate_site.py _site"
end

desc "Build and validate in one pass"
task :test => %w[build validate]

desc "Check outbound links (requires network access; never blocks deploys)"
task :linkcheck do
  sh "python3 scripts/check_external_links.py _site"
end

desc "Regenerate favicon and social-preview images"
task :brand_assets do
  sh "python3 scripts/generate_brand_assets.py"
end

task :default => :test
