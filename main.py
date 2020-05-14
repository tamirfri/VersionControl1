from shutil import copytree, rmtree
from pathlib import Path

# globally
def update_external_dependencies(*external):
  assert isinstance(external[0], str)
  print("Updates globally external packages:", ', '.join(external))
  print("\tmeanwhile does nothing")

# hierarchical
def update_internal_dependencies(package_name, *with_packages):
  assert isinstance(package_name, str)
  if not with_packages:
    print("No internal depenencies in", package_name)
    return
  assert isinstance(with_packages[0], str)
  internal_packages = Path('internal_packages')
  dst = internal_packages/package_name
  for pkg in with_packages:
    src = internal_packages/pkg
    copytree(src, dst/pkg, dirs_exist_ok=True)
    print("Updated", pkg, "in", package_name)

# application
def install_package(package_name):
  application = Path('application')
  temp_to_deploy = Path('temp_to_deploy')
  temp_to_destroy = Path('temp_to_destroy')
  internal_packages = Path('internal_packages')
  # begin deliver
  copytree(internal_packages/package_name, temp_to_deploy, dirs_exist_ok=True)
  print("Delivered:copied", package_name, "to", temp_to_deploy)
  # end deliver
  # begin deploy
  application.replace(temp_to_destroy)
  temp_to_deploy.replace(application)
  print("Deployed:replaced", temp_to_deploy, "to", application)
  rmtree(temp_to_destroy)
  # end deploy

def _parse_dependencies(file_name='dependencies.txt'):
  with open(file_name) as f:
    lines = tuple(l.split(':') for l in f if ':' in l)
  assert all(len(l)==2 for l in lines) # ':' should appear only once
  assert len(lines)%3 == 0 # lines come in triples
  # begin parse externals
  external = set() # appear only once
  for l in lines[2::3]:
    for pkg in map(str.strip, l[-1].split(',')):
      if pkg != 'None':
        external.add(pkg.strip())
  external = tuple(sorted(external))
  # end parse externals
  # begin parse internals
  internal = dict()
  for key, values in zip(lines[0::3], lines[1::3]):
    key = key[0].strip()
    assert key not in internal
    values = set(map(str.strip, values[-1].split(',')))
    values.discard('None')
    internal[key] = tuple(sorted(values))
  # end parse internals
  return (external, internal)

if __name__ == '__main__':
  print("My Tests:")
  external, internal = _parse_dependencies()
  print(f"external = {external}")
  print(f"internal = {internal}")
  update_external_dependencies(*external)
  update_internal_dependencies("P1", *internal["P1"])
  update_internal_dependencies("P2", *internal["P2"])
  update_internal_dependencies("P3", *internal["P3"])
  install_package("P2")
  install_package("P3")