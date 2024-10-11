from datetime import datetime
from appwrite.client import Client
from appwrite.services.databases import Databases
from src.config import AppwriteConfig
from src.exceptions import AppwriteDatabaseManagerError
from appwrite.id import ID

class AppwriteAPI:
    def __init__(self, config: AppwriteConfig):
        self.client = Client()
        self.client.set_endpoint(config.api_endpoint).set_project(config.project_id).set_key(config.api_key)
        self.databases = Databases(self.client)
        self.database_id = config.database_id

    def create_collection(self, class_info: dict):
        try:
            
            collection = self.databases.create_collection(
                database_id=self.database_id,
                collection_id=ID.unique(),
                name=class_info['name']
            )
            
            for attr in class_info['attributes']:
                self.create_attribute(collection['$id'], attr,)
            
            print(f"Collection '{class_info['name']}' created successfully.")
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to create collection: {str(e)}")
    
    def list_collections(self):
        try:
            collections = self.databases.list_collections(self.database_id)
            return collections['collections']
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to list collections: {str(e)}")
        
    def update_collection(self, collection_id: str, class_info: dict):
        #TODO: update method is not working properly. test and fix it
        try:
            # Update collection name if necessary
            self.databases.update_collection(
                database_id=self.database_id,
                collection_id=collection_id,
                name=class_info['name']
            )
            
            # Get existing attributes
            existing_attributes = self.databases.list_attributes(self.database_id, collection_id)
            print(existing_attributes)
            
            # Update or create attributes
            for attr in class_info['attributes']:
                existing_attr = next((a for a in existing_attributes['attributes'] if a['key'] == attr['key']), None)
                if existing_attr:
                    self.update_attribute(collection_id, attr, existing_attr)
                else:
                    self.create_attribute(collection_id, attr)
            
            print(f"Collection '{collection_id}' updated successfully.")
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to update collection: {str(e)}")
  
    def create_attribute(self, collection_id: str, attr: dict):
        try:
            attr_type = attr['type'].lower()
            if attr_type == 'stringattribute':
                self.databases.create_string_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    size=attr.get('size', 255),
                    required=attr.get('required', False),
                    default=attr.get('default', None),
                    array=attr.get('array', False)
                    
                )
            elif attr_type == 'integerattribute':
                self.databases.create_integer_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    required=attr.get('required', False),
                    min=attr.get('min'),
                    max=attr.get('max'),
                    default=attr.get('default', None),
                    array=attr.get('array', False)
                )
            elif attr_type == 'floatattribute':
                self.databases.create_float_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    required=attr.get('required', False),
                    min=attr.get('min'),
                    max=attr.get('max'),
                    default=attr.get('default', None),
                    array=attr.get('array', False)
                )
            elif attr_type == 'booleanattribute':
                self.databases.create_boolean_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    required=attr.get('required', False),
                    default=attr.get('default', None),
                    array=attr.get('array', False)
                )
            elif attr_type == 'datetimeattribute':
                default = attr.get('default', None)
                if default == 'Now':
                    default = datetime.now().isoformat()
                else:
                    default = None
                self.databases.create_datetime_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    required=attr.get('required', False),
                    default=default,
                    array=attr.get('array', False)
                )
            elif attr_type == 'emailattribute':
                    self.databases.create_email_attribute(
                        database_id=self.database_id,
                        collection_id=collection_id,
                        key=attr['key'],
                        required=attr.get('required', False),
                        default=attr.get('default', None),
                        array=attr.get('array', False)
                    )
            elif attr_type == 'ipaddressattribute':
                print('-==========>', attr_type)
                self.databases.create_ip_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    required=attr.get('required', False),
                    default=attr.get('default', None),
                    array=attr.get('array', False)
                )
            elif attr_type == 'enumattribute':
                self.databases.create_enum_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=attr['key'],
                    elements=attr.get('elements', []),
                    required=attr.get('required', False),
                    default=attr.get('default', None),
                    array=attr.get('array', False),
                    
                )
            elif attr_type == 'relationshipattribute':
                self.databases.create_relationship_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    related_collection_id=attr.get('related_collection_id', None),
                    type=attr.get('type', None),
                    two_way=attr.get('two_way', False),
                    key=attr['key'],
                    two_way_key=attr.get('two_way_key', None),
                    on_delete=attr.get('on_delete', None),
                )
                
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to create attribute: {str(e)}")

    def update_attribute(self, collection_id: str, updated_attr: dict, old_attr: dict):
        try:
            updated_attr_type = updated_attr['type'].lower()
            if updated_attr == 'stringattribute':
                self.databases.update_string_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    required=updated_attr.get('required', old_attr.get('required', False)),
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                )
            elif updated_attr_type == 'integerattribute':
                self.databases.update_integer_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    required=updated_attr.get('required', old_attr.get('required', False)),
                    min=updated_attr.get('min', old_attr.get('min')),
                    max=updated_attr.get('max', old_attr.get('max')),
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                )
            elif updated_attr_type == 'floatattribute':
                self.databases.update_float_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    required=updated_attr.get('required', old_attr.get('required', False)),
                    min=updated_attr.get('min', old_attr.get('min')),
                    max=updated_attr.get('max', old_attr.get('max')),
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                )
            elif updated_attr_type == 'booleanattribute':
                self.databases.update_boolean_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    required=updated_attr.get('required', old_attr.get('required', False)),
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                )
            elif updated_attr_type == 'datetimeattribute':
                default = updated_attr.get('default', old_attr.get('default', None)),
                if default == 'Now':
                    default = datetime.now().isoformat()
                else:
                    default = None
                self.databases.update_datetime_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    required=updated_attr.get('required', False),
                    default=default,
                    
                )
            elif updated_attr_type == 'emailattribute':
                    self.databases.update_email_attribute(
                        database_id=self.database_id,
                        collection_id=collection_id,
                        key=updated_attr['key'],
                        default=updated_attr.get('default', old_attr.get('default', None)),
                        
                    )
            elif updated_attr_type == 'ipaddressattribute':
                self.databases.update_ip_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                )
            elif updated_attr_type == 'enumattribute':
                self.databases.update_enum_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr['key'],
                    elements=updated_attr.get('elements', old_attr.get('elements', [])),
                    default=updated_attr.get('default', old_attr.get('default', None)),
                    
                    
                )
            elif updated_attr_type == 'relationshipattribute':
                self.databases.update_relationship_attribute(
                    database_id=self.database_id,
                    collection_id=collection_id,
                    key=updated_attr_type['key'],
                    on_delete=updated_attr.get('on_delete', None),
                )    
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to update attribute {updated_attr['key']} : {str(e)}")