"""Engineering role operationalization, not a new owner dimensional rule.
Exact source full-width connector and source hall junction supporting margins.
Only valid after actual359 source gate and fresh all-target/operation checks.
"""
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area,source_sweeps

def prove(record,unit,component_rows,source_rows):
 m=record['candidate']['model'];uid=unit['id'];proposal=record['trace']['proposal'];beds=[rect(proposal['rectangles']['bed'+str(i)])for i in (1,2,3)];L=F(record['candidate']['request']['L']);body=F(m['profile']['body_m']);T=F('.15');rear=max(r[3]for r in beds)+T;front=beds[0][1]
 cl=[x for x in m['source_hall_clamp359']if x['unit']==uid]
 if len(cl)!=1:raise ValueError('SOURCE_CLAMP_INVENTORY')
 hall=rect(cl[0]['proof']['hall']);private=list(map(rect,unit['rooms']['private_circulation']));d=[x for x in m['private_domains']if x['unit']==uid]
 if len(d)!=1 or set(d[0]['paths'])!={uid+'.bed'+str(i)for i in (1,2,3)}:raise ValueError('ALL_PRIVATE_PORT_TARGETS_REQUIRED')
 deps=['body_route_sweeps','door_operation','closet_operation','private_grouping','fixture_inventory_use','circulation_functional_integrity']
 if any(source_rows[k]['status']!='PASS_LIMITED'for k in deps):raise ValueError('FRESH_MARGIN_FUNCTION_PREREQUISITES')
 def tr(q):
  a,b,c,d=q;return (a,b,c,d)if uid=='A'else(a,L-d,c,L-b)
 groups=[]
 for i,(a,b)in enumerate(zip(beds,beds[1:])):
  connector=(a[2]+T,front,b[0]-T,rear);junction=intersection((connector[0],hall[1],connector[2],hall[3]),hall)
  if connector[2]-connector[0]<body or junction is None:raise ValueError('SOURCE_FULL_WIDTH_CONNECTOR_REQUIRED')
  domain=[tr(connector),tr(junction)]
  if difference(domain,private):raise ValueError('SOURCE_CONNECTOR_JUNCTION_OUTSIDE_ACTUAL_FLOOR')
  traversals=[]
  for target,path in d[0]['paths'].items():
   ports=[p for p in m['module_ports']if p['opening_id']==target+'.entry']
   if len(ports)!=1 or list(map(F,path[-1]))!=list(map(F,ports[0]['center'])):raise ValueError('ACTUAL_SOURCE_PORT_ENDPOINT')
   sw=source_sweeps(path,body)
   if any(intersection(x,y)for x in domain for y in sw):traversals.append({'target_port':target+'.entry','path_digest':digest(path),'source_port_digest':digest(ports[0])})
  if not traversals:raise ValueError('SOURCE_CONNECTOR_WITHOUT_CHECKED_REQUIRED_TRAVERSAL')
  groups.append({'source_connector_index':i,'source_connector':list(map(str,tr(connector))),'source_junction':list(map(str,tr(junction))),'required_traversals':traversals,'source_origin':'SOURCE359 full-width connector derived from actual source-bedroom gaps; same source hall junction, no longitudinal extension outside those boundaries'})
 allowed=[rect(g[k])for g in groups for k in('source_connector','source_junction')];claims=[]
 for c in component_rows:
  for qraw in c['unsupported_margin_regions']:
   q=rect(qraw);missing=difference([q],allowed);matching=[i for i,g in enumerate(groups)if any(intersection(q,rect(g[k]))for k in('source_connector','source_junction'))]
   claims.append({'region':qraw,'source_connector_groups':matching,'uncovered_regions':[list(map(str,x))for x in missing],'verdict':'PASS_SCOPED_SOURCE_CONNECTOR_PORTAL_JUNCTION_MARGIN'if not missing and matching else'UNKNOWN_OUTSIDE_SOURCE_MARGIN'})
 return {'schema':'SOURCE359_CONNECTOR_MARGIN_ROLE','model_hash':digest(m),'unit':uid,'classification':'ENGINEERING_ROLE_OPERATIONALIZATION','source_row_digests':{k:digest(source_rows[k])for k in deps},'source_clamp_digest':digest(cl[0]),'groups':groups,'claims':claims,'all_residual_cells_source_bound':bool(claims)and all(c['verdict'].startswith('PASS_')for c in claims),'necessity_claimed':False,'scope':'A whole actual connector/portal junction can serve a checked required traversal without every floor point being a body sweep. No added terminal branch or outside longitudinal extension accepted. Q04 finite comparison remains separate.'}
