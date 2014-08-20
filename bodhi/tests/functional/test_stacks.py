# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from datetime import datetime, timedelta
from webtest import TestApp

import bodhi.tests.functional.base

from bodhi import main
from bodhi.models import (
    Base,
    Bug,
    Build,
    CVE,
    DBSession,
    Group,
    Package,
    Release,
    Update,
    UpdateType,
    UpdateStatus,
    UpdateRequest,
    Stack,
)


class TestStacksService(bodhi.tests.functional.base.BaseWSGICase):

    def setUp(self):
        super(TestStacksService, self).setUp()
        self.session = session = DBSession()
        package = Package(name=u'gnome-shell')
        session.add(package)
        session.flush()
        stack = Stack(name=u'GNOME', packages=[package])
        session.add(stack)
        session.flush()

    def test_404(self):
        self.app.get('/stacks/watwatwat', status=404)

    def test_get_single_stack(self):
        res = self.app.get('/stacks/GNOME')
        self.assertEquals(res.json_body['stack']['name'], u'GNOME')
        self.assertEquals(res.json_body['stack']['packages'][0]['name'], u'gnome-shell')

    def test_list_stacks(self):
        res = self.app.get('/stacks/')
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], u'GNOME')
        self.assertEquals(body['stacks'][0]['packages'][0]['name'], u'gnome-shell')

    def test_list_stacks_with_pagination(self):
        # Create a second stack
        pkg1 = Package(name=u'firefox')
        pkg2 = Package(name=u'xulrunner')
        self.session.add(pkg1)
        self.session.add(pkg2)
        self.session.flush()
        ff = Stack(name=u'Firefox', packages=[pkg1, pkg2])
        self.session.flush()

        res = self.app.get('/stacks/')
        body = res.json_body
        self.assertEquals(len(body['stacks']), 2)

        res = self.app.get('/stacks/', {'rows_per_page': 1})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], u'GNOME')

        res = self.app.get('/stacks/', {'rows_per_page': 1, 'page': 2})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], 'Firefox')
        self.assertEquals(body['stacks'][0]['packages'][0]['name'], 'firefox')

    def test_list_stacks_by_name(self):
        res = self.app.get('/stacks/', {'name': 'GNOME'})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], 'GNOME')

    def test_list_stacks_by_name_mismatch(self):
        res = self.app.get('/stacks/', {'like': '%KDE%'})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 0)

    def test_list_stacks_by_name_match(self):
        res = self.app.get('/stacks/', {'like': '%GN%'})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], 'GNOME')

    def test_list_stacks_by_package_name(self):
        res = self.app.get('/stacks/', {"packages": 'gnome-shell'})
        body = res.json_body
        self.assertEquals(len(body['stacks']), 1)
        self.assertEquals(body['stacks'][0]['name'], 'GNOME')

    def test_list_stacks_by_nonexistant_package(self):
        res = self.app.get('/stacks/', {"packages": 'carbunkle'}, status=400)
        self.assertEquals(res.json_body['errors'][0]['name'], 'packages')
        self.assertEquals(res.json_body['errors'][0]['description'],
                          'Invalid packages specified: carbunkle')

    def test_new_stack(self):
        attrs = {'name': 'KDE', 'packages': 'kde-filesystem kdegames'}
        res = self.app.post("/stacks/", attrs, status=200)
        body = res.json_body
        self.assertEquals(body['name'], 'KDE')
        r = self.session.query(Stack).filter(Stack.name==attrs["name"]).one()
        self.assertEquals(r.name, 'KDE')
        self.assertEquals(len(r.packages), 2)
        self.assertEquals(r.packages[0].name, 'kde-filesystem')

    def test_new_stack_invalid_name(self):
        attrs = {"name": ""}
        res = self.app.post("/stacks/", attrs, status=400)
        self.assertEquals(res.json_body['status'], 'error')
