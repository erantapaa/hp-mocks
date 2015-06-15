import re
from _file_util import read_file, write_file

class Page():
  def __init__(self, header, end_head, topbody, footer, epilogue, tail):
    self.header          = header       # a string
    self.after_header    = []
    self.end_head        = end_head
    self.topbody         = topbody
    self.body            = []
    self.footer          = footer       # a string
    self.before_epilogue = []
    self.epilogue        = epilogue     # a string
    self.after_epilogue  = []
    self.tail            = tail
    self._body_class     = None
    pass

  def add_css(self, url):
    css = '  <link href="{}" type="{}" rel="{}">'.format(url, "text/css", "stylesheet")
    self.after_header.append(css)

  def add_js(self, url):
    js = '  <script href="{}"></script>'.format(url)
    self.after_header.append(js)

  def use_jquery(self):
    self.prepend_epilogue('<script src="/static/js/jquery.js"></script>')

  def prepend_epilogue(self, s):
    self.before_epilogue.append(s)

  def append_epilogue(self, s):
    self.after_epilogue.append(s)

  def append_body(self, s):
    self.body.append(s)

  def body_class(self, cls):
    self._body_class = cls

  def compose(self):
    """Return the composed page."""
    if self._body_class:
      body_tag = '<body class="{}">'.format(self._body_class)
    else:
      body_tag = '<body>'
    parts = [self.header]                                             \
              + self.after_header                                     \
              + [ "<!-- end header -->", self.end_head, body_tag ]    \
              + [ self.topbody, "<!-- end topbody -->" ]              \
              + self.body                                             \
              + [ self.footer, "<!-- end footer -->" ]                \
              + self.before_epilogue                                  \
              + [ self.epilogue ]                                     \
              + self.after_epilogue                                   \
              + [ "<!-- end epilogue -->", self.tail ]                \

    page = ''.join(parts)
    return page

"""
<!-- end header -->
<!-- end topbody -->
<!-- end footer -->
<!-- end epilogue -->
"""

def make_template(contents):
  """Make a Page object from a template file."""
  pat = "(.*?)<!-- end header -->(\s*</head>\s*)<body.*?>(.*?)<!-- end topbody -->(.*?)<!-- end footer -->(.*?)<!-- end epilogue -->(.*)"
  m = re.match(pat, contents, re.S)
  if not m:
    raise "unable to parse template"
  header   = m.group(1)
  end_head = m.group(2)
  topbody  = m.group(3)
  footer   = m.group(4)
  epilogue = m.group(5)
  tail     = m.group(6)

  p = Page(header, end_head, topbody, footer, epilogue, tail)
  return p

