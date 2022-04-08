#
#      RESCS SHACL Shapes: Build Tools for the RESCS SHACL Shapes Library
#      Copyright (C) 2022  Tobias Schweizer, Kurt Baumann, Laura Rettig
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as published
#      by the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

def absolute_from_rel_file_path(relative_path: str, file_location: str) -> str:
    """
    Given a path relative to file_location,
    returns the absolute path.

    :param relative_path: The path relative to the file_location param.
    :param file_location: The location of the file this method is called from.
    :return: The absolute path.
    """
    dirname = os.path.dirname(file_location)
    return os.path.join(dirname, relative_path)
