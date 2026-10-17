import copy,html,importlib.util,json,pathlib,sys,tempfile,unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import mod_overview as m

class ModOverview(unittest.TestCase):
    def test_merged_snapshot_available_without_developer_clones(self):
        data=m.snapshot(m.read_json(ROOT/'templates/overview/catalog.json'),None)
        mods={row['id']:row for row in data['mods']}
        for ident,version in [('qm','0.18.0-dev.1'),('rooms','0.2.0-dev.6')]:
            row=mods[ident]
            self.assertEqual(row['version'],version)
            self.assertFalse(row['installed'])
            self.assertIn('NOT INSTALLED',row['review'])
            self.assertEqual(len(row['source_commit']),40)
            self.assertIn('G7/stable G8 BLOCKED',row['limits'])
        self.assertFalse(any(f['status']=='Separate branch' for f in mods['qm']['features']))
        records=next(f for f in data['flows'] if f['name']=='Physical storage records')
        self.assertEqual(records['status'],'Source')
        allocation=next(f for f in data['flows'] if f['name']=='Advisory room allocation')
        self.assertEqual(allocation['status'],'Foundation')
        self.assertIn('remain disabled',allocation['text'])
        self.assertTrue(any(e['a']=='rooms' and e['b']=='qm' and e['kind']=='Required' for e in data['edges']))

    def test_watch_refreshes_after_source_edit(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td);root,a,b,catalog=self.fixture(p)
            cat=p/'catalog.json';cat.write_text(json.dumps(catalog))
            template=p/'template.json';template.write_text(json.dumps({'html':'<div data-srcdoc="__B47_PORTFOLIO_DATA__"></div>'}))
            output=p/'Output';calls=[]
            def advance(_):
                if calls:raise KeyboardInterrupt
                calls.append(1);(a/'VERSION').write_text('2.0.0')
            with mock.patch.object(sys,'argv',['overview','--catalog',str(cat),'--template',str(template),'--repositories',str(root),'--output',str(output),'--watch']),mock.patch.object(m,'git',return_value=None),mock.patch.object(m.time,'sleep',side_effect=advance),self.assertRaises(KeyboardInterrupt):m.main()
            data=json.loads((output/'portfolio.json').read_text())
            self.assertEqual(data['mods'][0]['version'],'2.0.0')
            self.assertIn('REVIEW',data['mods'][0]['review'])
    def fixture(self,base):
        root=base/'Mods';a=root/'First';b=root/'Second'
        for p,modid in [(a,'FirstID'),(b,'SecondID')]:
            (p/'src'/'42').mkdir(parents=True)
            (p/'src'/'42'/'mod.info').write_text('id='+modid+'\n'+('require=FirstID,ExternalMod\n' if p==b else ''))
            (p/'src'/'42'/'code.lua').write_text('return 1')
            (p/'README.md').write_text('Feature documentation')
            (p/'VERSION').write_text('1.0.0')
            (p/'AGENTS.md').write_text('custom instructions')
            (p/'local.settings.json').write_text('private settings')
        catalog=dict(mods=[dict(id=id,folder=p.name,name=p.name,mod_ids=[mid],features=[dict(status='Foundation',text='Test feature')],limits='Runtime untested',evidence=['README.md'],source_roots=['src'],source_digest=m.fingerprint(p,['src','README.md','VERSION'])) for p,id,mid in [(a,'a','FirstID'),(b,'b','SecondID')]],edges=[],flows=[])
        return root,a,b,catalog

    def test_live_versions_dependencies_and_no_project_writes(self):
        with tempfile.TemporaryDirectory() as td:
            root,a,b,catalog=self.fixture(pathlib.Path(td))
            before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with mock.patch.object(m,'git',return_value=None):data=m.snapshot(catalog,root)
            self.assertEqual(data['edges'][0]['a'],'a')
            self.assertEqual(data['mods'][1]['unresolved_requires'],['ExternalMod'])
            self.assertIn('SNAPSHOT MATCH',data['mods'][0]['review'])
            self.assertTrue(all(p.read_bytes()==raw for p,raw in before.items()))
            (a/'VERSION').write_text('1.1.0');(a/'src/42/code.lua').write_text('return 2')
            with mock.patch.object(m,'git',return_value=None):new=m.snapshot(catalog,root)
            self.assertEqual(new['mods'][0]['version'],'1.1.0')
            self.assertIn('REVIEW',new['mods'][0]['review'])

    def test_descriptor_edits_are_live_and_need_evidence_review(self):
        with tempfile.TemporaryDirectory() as td:
            root,a,b,catalog=self.fixture(pathlib.Path(td));(a/'docs').mkdir()
            d=dict(schema=1,id='a',name='First',version='1.0.0',reviewed=True,source_digest=m.fingerprint(a,['src','README.md','VERSION']),features=[dict(status='Planned',text='Future feature')],evidence=['README.md'],relations=[dict(target='b',kind='Optional',text='Provider contract')])
            (a/'docs/MOD_OVERVIEW.json').write_text(json.dumps(d))
            with mock.patch.object(m,'git',return_value=None):data=m.snapshot(catalog,root)
            self.assertIn('CURRENT DESCRIPTOR',data['mods'][0]['review'])
            self.assertEqual(data['mods'][0]['features'][0]['status'],'Planned')
            self.assertTrue(any(e['a']=='b' and e['b']=='a' and e['kind']=='Optional' for e in data['edges']))
            (a/'src/42/code.lua').write_text('return 8')
            with mock.patch.object(m,'git',return_value=None):data=m.snapshot(catalog,root)
            self.assertIn('REVIEW',data['mods'][0]['review'])
            d['evidence']=['../secret'];(a/'docs/MOD_OVERVIEW.json').write_text(json.dumps(d))
            with mock.patch.object(m,'git',return_value=None),self.assertRaises(ValueError):m.snapshot(catalog,root)

    def test_worktrees_dedup_new_and_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root,a,b,catalog=self.fixture(pathlib.Path(td))
            (root/'.worktrees/hidden/src').mkdir(parents=True)
            (root/'.worktrees/hidden/src/mod.info').write_text('id=Hidden')
            duplicate=root/'Duplicate';(duplicate/'src').mkdir(parents=True);(duplicate/'src/mod.info').write_text('id=FirstID')
            new=root/'New';(new/'src').mkdir(parents=True);(new/'src/mod.info').write_text('id=NewID')
            with mock.patch.object(m,'git',return_value=None):data=m.snapshot(catalog,root)
            self.assertEqual(len(data['mods']),3)
            self.assertEqual(data['mods'][-1]['features'][0]['status'],'UNKNOWN')
            missing=m.snapshot(catalog,None)
            self.assertTrue(all(not x['installed'] for x in missing['mods']))

    def test_safe_export_and_custom_output_preservation(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td);_,_,_,catalog=self.fixture(p)
            catalog['mods'][0]['features'][0]['text']='</script><script>alert("x")</script>'
            template={'html':'<div data-srcdoc="__B47_PORTFOLIO_DATA__"></div>'}
            exported=m.render(catalog,template)
            self.assertNotIn('<script>',exported)
            output=p/'Output';m.write_snapshot(catalog,template,output)
            m.write_snapshot(catalog,template,p/'unused/../Output')
            old=(output/'portfolio.json').read_bytes()
            (output/'index.html').write_text('custom')
            with self.assertRaises(ValueError):m.write_snapshot(catalog,template,output)
            self.assertEqual((output/'index.html').read_text(),'custom')
            self.assertEqual((output/'portfolio.json').read_bytes(),old)

    def test_catalog_portable_and_export_marker(self):
        c=m.read_json(ROOT/'templates/overview/catalog.json');m.validate_catalog(c)
        self.assertEqual(len(c['mods']),26)
        self.assertNotIn('C:/Users/',json.dumps(c))
        t=m.read_json(ROOT/'templates/overview/view.json')
        self.assertEqual(t['html'].count('__B47_PORTFOLIO_DATA__'),1)

    def test_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)
            with self.assertRaises(ValueError):m.safe_path(p,'../outside')
            with self.assertRaises(ValueError):m.safe_path(p,p/'absolute')
            outside=p/'outside';outside.mkdir()
            try:(p/'link').symlink_to(outside,target_is_directory=True)
            except OSError:return
            with self.assertRaises(ValueError):m.safe_path(p,'link/file')
