#!/usr/bin/python3
'''
   Copyright 2020 Ian Santopietro (ian@system76.com)

   This file is part of Repoman.

    Repoman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Repoman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Repoman.  If not, see <http://www.gnu.org/licenses/>.
'''

import repolib

def get_repo_for_name(name):
    """ Get a repo from a given name.

    This takes a name and gives back a repolib.Source object which represents 
    the given source.

    Arguments:
        name (str): The name of the repo to look for.
    
    Returns:
        A repolib.Source (or subclass) representing the given name.
    """
    full_path = repolib.util.get_source_path(name)
    if full_path:
        if full_path.suffix == '.sources':
            repo = repolib.Source(filename=full_path)
        else:
            repo = repolib.LegacyDebSource(filename=full_path)
        
        return repo
    raise Exception(f'Could not find a source for {name}.')

def get_all_sources(get_system=False):
    """ Returns a dict with all sources on the system.
    
    The keys for each entry in the dict are the names of the sources.
    The values are the corresponding repolin.Source subclass

    Arguments:
        get_system (bool): whether to include the system sources or not.
    
    Returns:
        The above described dict.
    """
    sources = {}

    if get_system:
        try:
            system = get_repo_for_name('system')
            sources['system'] = system
        except Exception:
            pass
    
    sources_dir = repolib.util.get_sources_dir()
    files_sources = sources_dir.glob('*.sources')
    files_list = sources_dir.glob('*.list')

    for file in files_sources:
        repo = repolib.Source(filename=file)
        repo.load_from_file()
        name = repo.filename.replace('.sources', '')
        sources[name] = repo
    
    for file in files_list:
        repo = repolib.LegacyDebSource(filename=file)
        repo.load_from_file()
        name = repo.filename.replace('.list', '')
        sources[name] = repo
    
    return sources
        