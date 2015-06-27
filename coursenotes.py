#course notes generation, using jinja2 for templates
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import os
import jinja2
import webapp2


#creates file folder, then initiates instance for jinja environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


DEFAULT_CARDLIST_NAME = 'default_cardlist'
DEFAULT_COMMENTS_NAME = 'default_comments'
# DEFAULT_STAGE_NAME = 'default_stage'
# DEFAULT_WORKSESSION_NAME = 'default_worksession'

#set parent keys to include entities in same entity groups
def cardlist_key(cardlist_name=DEFAULT_CARDLIST_NAME):
    """Constructs a Datastore key for a cardlist entity.
    We use cardlist_name as the key.
    """
    return ndb.Key('Cardlist', cardlist_name)

def comments_key(comments_name=DEFAULT_COMMENTS_NAME):
    """Constructs a Datastore key for a comments entity.
    We use comments_name as the key.
    """
    return ndb.Key('Comments', comments_name)

# def stage_key(stage_name=DEFAULT_STAGE_NAME):
#     """Constructs a Datastore key for a stage entity.
#     We use stage_name as the key.
#     """
#     return ndb.Key('Stage', stage_name)

# def worksession_key(worksession_name=DEFAULT_WORKSESSION_NAME):
#     """Constructs a Datastore key for a worksession entity.
#     We use worksession_name as the key.
#     """
#     return ndb.Key('Worksession', worksession_name)

#entity classes
# class Stage(ndb.Model):
#   """Sub model for representing a stage."""
#   name = ndb.StringProperty(indexed=True)
#   order = ndb.IntegerProperty(indexed=True)

# class Worksession(ndb.Model):
#   """A main model for representing a worksession."""
#   stage = ndb.StructuredProperty(Stage)
#   name = ndb.StringProperty(indexed=True)
#   order = ndb.IntegerProperty(indexed=True)

class Card(ndb.Model):
  """A main model for representing a card."""
  # worksession = ndb.StructuredProperty(Worksession)
  title = ndb.StringProperty(indexed=True)
  content = ndb.TextProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)

class Author(ndb.Model):
  """Sub model for representing an author."""
  identity = ndb.StringProperty(indexed=True)
  name = ndb.StringProperty(indexed=False)
  email = ndb.StringProperty(indexed=False)

class Post(ndb.Model):
  """A main model for representing an individual post."""
  author = ndb.StructuredProperty(Author)
  active = ndb.BooleanProperty(indexed=True)
  date = ndb.DateTimeProperty(auto_now_add=True)
  content = ndb.StringProperty(indexed=False)

# Something for later...
# class Useful(ndb.Model):
#   """A main model for representing a useful flag."""
#   card = ndb.StructuredProperty(Card)
#   useful = ndb.BooleanProperty(indexed=True)
#   usefulanswer = ndb.BooleanProperty(indexed=True)


#stage 1, worksession 1 cards
card1 = Card(title = 'Reflection',
  content = '''My browser displays content fetched from a server via the internet over http or secure http. That content is wrapped up in HTML. HTML is  structured with a series of elements, most of which contain an opening and closing tag. Tags, and their attributes, apply human-centered styling to simple content (like bold, italics, or an image). Tags can be grouped into inline and block tags, the latter of which create containers that hold other elements.''')
card2 = Card(title = 'The Basics',
  content = '''<p>Reference <a href="http://www.w3schools.com/default.asp">W3 Schools</a> and <a href="http://www.google.com">Google</a> for just about anything.</p>
            <p>Element = opening tag + content + closing tag</p>
            <p>HTML Attributes = belong to tags<br>
              <span class="italic">e.g. &lt;tag attribute="value"&gt;contents&lt;/tag&gt;</span>
            <p>One great example would be a link to another site <a href="http://www.udacity.com">like this using the   <span class="bold">href</span> attribute</a> or an image using the <span class="bold">src</span> attribute:<br><br>
              <img class="image-center-responsive" src="http://thisisinfamous.com/wp-content/uploads/2015/01/jurassic-park-logo.jpg" alt="Jurassic Park gates"><br></p>
            <p>Just don't forget your <span class="bold">alt</span> tag; it will make someone's life better when viewing your page.</p>
            <p>Or using <span class="bold">iframe</span> to embed a video like this:<p>
            <div class="video-center-embed">
              <iframe width="420" height="315" src="https://www.youtube.com/embed/Bim7RtKXv90?rel=0" allowfullscreen></iframe>
            </div>''')
card3 = Card(title = 'Void Tags',
  content = '''<p>No content, so no closing tag<br>
              <span class="italic">e.g. Images &lt;img&gt;</span> or <span class="italic">Break &lt;br&gt;</span>
            </p>''')
card4 = Card(title = 'Inline versus Block',
  content = '''<p>Inline = Just end the line and wrap to the next<br>
          <span class="italic">e.g. Break &lt;br&gt;</span></p>
            <p>Block = Create invisible box that can have height and width<br>
          <span class="italic">e.g. Paragraph &lt;p&gt;</span></p>''')
card5 = Card(title = 'Container Tags',
  content = '''<p>Hold other elements<br>
          <span class="italic">e.g. Span &lt;span&gt; (inline)</span> or <span class="italic">Div &lt;div&gt; (block)</span></p>''')
card6 = Card(title = 'Lists and Menus',
  content = '''<p>Add <a href="http://www.w3schools.com/html/html_lists.asp">ordered, unordered, or HTML lists</a> for bullets, numbers/alpha, or menus; use CSS for styling to create tabbed menus or use alternative images for bullet points.</p>
            <p>Lists can be nested; here,the nested list is part of a list item from the parent list:</p>
            <p class="code">&lt;ul&gt;Parent List<br>
            &nbsp;&nbsp;&lt;li&gt;First Item&lt;/li&gt;<br>
            &nbsp;&nbsp;&lt;li&gt;Second Item&lt;/li&gt;<br>
            &nbsp;&nbsp;&lt;li&gt;Third Item with a nested list<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&lt;ul&gt;Nested List<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;li&gt;Nested First Item&lt;/li&gt;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;li&gt;Nested Second Item&lt;/li&gt;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&lt;/ul&gt;<br>
            &nbsp;&nbsp;&lt;/li&gt;<br>
            &nbsp;&nbsp;&lt;li&gt;Fourth Item&lt;/li&gt;<br>
            &lt;/ul&gt;</p>''')
card7 = Card(title = 'HTML Document Structure',
  content = '''<p>Simplified with HTML5, HTML documents follow this basic structure (but not needed for codepen...codepen just needs the typical &lt;body&gt; content):<br>
            <p class="code">&lt;!DOCTYPE HTML&gt; = doctype<br>
              &lt;html&gt; = opening html tag<br>
              &lt;head&gt; = metadata like js and css<br>
              &lt;title&gt; = title for browser window<br>
              &lt;body&gt; = content of doc</p>''')

#stage 1. worksession 2 cards
card8 = Card(title = 'Reflection',
  content = '''One word: boxify. With everything in HTML structured in rectangular boxes (even seemingly non-rectangular items), you can easily build or break-down a webpage into small, understandable parts. Classes provide the labeling for the boxes in your HTML structure, while CSS provides the styling.''')




#add all of the others...

#insert data for testing
# card1.put()
# card2.put()
# card3.put()
# card4.put()
# card5.put()
# card6.put()
# card7.put()
# card8.put()

# import time
# time.sleep(.1)


#handlers act as gatekeepers that direct you to the right path
class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  #finds file template and passes in parameters
  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  #sends template created back to browser
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class MainHandler(Handler):
  def get(self):
    querycard = Card.query().order(Card.date)
    cards = querycard.fetch()
    self.render("coursenotes.html", cards=cards)

# Logging
    error = self.request.get('error','')
    print '##### error will be here'
    print error
    print

    query = Card.query().order(Card.title)
    cards = query.fetch()
    print '##### length will be here'
    print len(cards)
    print
    print '##### the first fetched card will be here'
    print cards[0]
    print

    print '##### each card will be here'
    for card in query:
      print card
      print
    print '##### end testing'
    print


  # def post(self):
  #   self.render("coursenotes.html",
  #     stages = stages,
  #     worksessions = worksessions,
  #     cards=cards)

class AddHandler(Handler):
  def get(self):
    self.render("addcoursenotes.html")


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/addnotes', AddHandler)
  ], debug = True)





