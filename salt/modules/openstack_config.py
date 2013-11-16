# -*- coding: utf-8 -*-
'''
Modify, retrieve, or delete values from OpenStack configuration files.

:maintainer: Jeffrey C. Ollie <jeff@ocjtech.us>
:maturity: new
:depends:
:platform: linux

'''
import salt.utils
import salt.exceptions

from salt.utils.decorators import which as _which

try:
    from shlex import quote as _quote
except ImportError:
    try:
        from pipes import quote as _quote
    except ImportError:
        _quote = None

def __virtual__():
    global _quote
    if _quote is None:
        return False
    return 'openstack_config'

def _fallback(*args, **kw):
    return 'The "openstack-config" command needs to be installed for this function to work.  Typically this is included in the "openstack-utils" package.'

@_which('openstack-config')
def set(filename, section, parameter, value):
    '''
    Set a value in an OpenStack configuration file.

    filename
        The full path to the configuration file

    section
        The section in which the parameter will be set

    parameter
        The parameter to change

    value
        The value to set

    '''

    filename = _quote(filename)
    section = _quote(section)
    parameter = _quote(parameter)
    value = _quote(value)

    result = __salt__['cmd.run_all']('openstack-config --set {} {} {} {}'.format(filename, section, parameter, value))

    if result['retcode'] == 0:
        return result['stdout']
    else:
        raise salt.exceptions.CommandExecutionError(result['stderr'])

@_which('openstack-config')
def get(filename, section, parameter):
    '''
    Get a value from an OpenStack configuration file.

    filename
        The full path to the configuration file

    section
        The section from which to search for the parameter

    parameter
        The parameter to return

    CLI Example:

    .. code-block:: bash
        salt-call openstack_config.get /etc/keystone/keystone.conf sql connection

    '''

    filename = _quote(filename)
    section = _quote(section)
    parameter = _quote(parameter)

    result = __salt__['cmd.run_all']('openstack-config --get {} {} {}'.format(filename, section, parameter))

    if result['retcode'] == 0:
        return result['stdout']
    else:
        raise salt.exceptions.CommandExecutionError(result['stderr'])

@_which('openstack-config')
def delete(filename, section, parameter):
    '''
    Delete a value from an OpenStack configuration file.

    filename
        The full path to the configuration file

    section
        The section from which to delete the parameter

    parameter
        The parameter to delete

    '''

    filename = _quote(filename)
    section = _quote(section)
    parameter = _quote(parameter)

    result = __salt__['cmd.run_all']('openstack-config --del {} {} {}'.format(filename, section, parameter))

    if result['retcode'] == 0:
        return result['stdout']
    else:
        raise salt.exceptions.CommandExecutionError(result['stderr'])