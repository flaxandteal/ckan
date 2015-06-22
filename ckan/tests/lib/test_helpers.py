import nose
from pylons import config

import ckan.lib.helpers as h
import ckan.exceptions

eq_ = nose.tools.eq_
CkanUrlException = ckan.exceptions.CkanUrlException


class TestHelpersUrlForStatic(object):

    def test_url_for_static(self):
        url = '/assets/ckan.jpg'
        eq_(h.url_for_static(url), url)

    def test_url_for_static_adds_starting_slash_if_url_doesnt_have_it(self):
        slashless_url = 'ckan.jpg'
        url = '/' + slashless_url
        eq_(h.url_for_static(slashless_url), url)

    def test_url_for_static_converts_unicode_strings_to_regular_strings(self):
        url = u'/ckan.jpg'
        assert isinstance(h.url_for_static(url), str)

    def test_url_for_static_raises_when_called_with_external_urls(self):
        url = 'http://assets.ckan.org/ckan.jpg'
        nose.tools.assert_raises(CkanUrlException, h.url_for_static, url)

    def test_url_for_static_raises_when_called_with_protocol_relative(self):
        url = '//assets.ckan.org/ckan.jpg'
        nose.tools.assert_raises(CkanUrlException, h.url_for_static, url)


class TestHelpersUrlForStaticOrExternal(object):

    def test_url_for_static_or_external(self):
        url = '/assets/ckan.jpg'
        eq_(h.url_for_static_or_external(url), url)

    def test_url_for_static_or_external_works_with_external_urls(self):
        url = 'http://assets.ckan.org/ckan.jpg'
        eq_(h.url_for_static_or_external(url), url)

    def test_url_for_static_or_external_converts_unicode_to_strings(self):
        url = u'/ckan.jpg'
        assert isinstance(h.url_for_static_or_external(url), str)

    def test_url_for_static_or_external_adds_starting_slash_if_needed(self):
        slashless_url = 'ckan.jpg'
        url = '/' + slashless_url
        eq_(h.url_for_static_or_external(slashless_url), url)

    def test_url_for_static_or_external_works_with_protocol_relative_url(self):
        url = '//assets.ckan.org/ckan.jpg'
        eq_(h.url_for_static_or_external(url), url)


class TestHelpersRenderMarkdown(object):

    def test_render_markdown_allow_html(self):
        data = '<h1>moo</h1>'
        eq_(h.render_markdown(data, allow_html=True), data)

    def test_render_markdown_not_allow_html(self):
        data = '<h1>moo</h1>'
        output = '<p>moo\n</p>'
        eq_(h.render_markdown(data), output)

    def test_render_markdown_auto_link_without_path(self):
        data = 'http://example.com'
        output = '<p><a href="http://example.com" target="_blank" rel="nofollow">http://example.com</a>\n</p>'
        eq_(h.render_markdown(data), output)

    def test_render_markdown_auto_link(self):
        data = 'https://example.com/page.html'
        output = '<p><a href="https://example.com/page.html" target="_blank" rel="nofollow">https://example.com/page.html</a>\n</p>'
        eq_(h.render_markdown(data), output)

    def test_render_markdown_auto_link_ignoring_trailing_punctuation(self):
        data = 'My link: http://example.com/page.html.'
        output = '<p>My link: <a href="http://example.com/page.html" target="_blank" rel="nofollow">http://example.com/page.html</a>.\n</p>'
        eq_(h.render_markdown(data), output)


class TestHelpersRemoveLineBreaks(object):

    def test_remove_linebreaks_removes_linebreaks(self):
        test_string = 'foo\nbar\nbaz'
        result = h.remove_linebreaks(test_string)

        assert result.find('\n') == -1,\
            '"remove_linebreaks" should remove line breaks'

    def test_remove_linebreaks_casts_into_str(self):
        class StringLike(str):
            pass

        test_string = StringLike('foo')
        result = h.remove_linebreaks(test_string)

        strType = ''.__class__
        assert result.__class__ == strType,\
            '"remove_linebreaks" casts into str()'


class TestLicenseOptions(object):
    def setup(self):
        config['ckan.licenses_offered'] = None
        config['ckan.licenses_offered_exclusions'] = None

    @classmethod
    def teardown_class(cls):
        config['ckan.licenses_offered'] = None
        config['ckan.licenses_offered_exclusions'] = None

    def test_default_list(self):
        licenses = h.license_options()
        eq_(dict(licenses)['CC-BY-4.0'], 'Creative Commons Attribution 4.0')

    def test_sort(self):
        licenses = h.license_options()
        titles = [l[1] for l in licenses]
        eq_(titles[:-1], sorted(titles[:-1]))
        eq_(titles[-1], 'License not specified')

    def test_configured_list(self):
        config['ckan.licenses_offered'] = 'CC0-1.0 CC-BY-4.0'
        licenses = h.license_options()
        eq_(licenses, [('CC0-1.0', 'Creative Commons Zero 1.0'),
                       ('CC-BY-4.0', 'Creative Commons Attribution 4.0')])

    def test_default_exclusions(self):
        licenses = h.license_options()
        assert 'cc-by' not in dict(licenses)

    def test_configured_exclusions(self):
        config['ckan.licenses_offered_exclusions'] = 'CC0-1.0 CC-BY-4.0'
        licenses = h.license_options()
        assert 'CC0-1.0' not in dict(licenses)
        assert 'CC-BY-4.0' not in dict(licenses)
        assert 'CC-BY-SA-4.0' in dict(licenses)

    def test_includes_existing_license(self):
        licenses = h.license_options('some-old-license')
        eq_(dict(licenses)['some-old-license'], 'some-old-license')
        # and it is first on the list
        eq_(licenses[0][0], 'some-old-license')

    def test_gets_correct_title_for_excluded_license(self):
        licenses = h.license_options('cc-by')
        eq_(dict(licenses)['cc-by'], 'Creative Commons Attribution')
