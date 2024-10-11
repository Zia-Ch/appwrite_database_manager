from datetime import datetime
from typing import Dict, Any, List, Optional
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from src.config import AppwriteConfig
from src.exceptions import AppwriteDatabaseManagerError

class AppwriteAPI:
    def __init__(self, config: AppwriteConfig):
        self.client = Client()
        self.client.set_endpoint(config.api_endpoint).set_project(config.project_id).set_key(config.api_key)
        self.databases = Databases(self.client)
        self.database_id = config.database_id

    def create_collection(self, class_info: Dict[str, Any]) -> None:
        try:
            collection = self.databases.create_collection(
                database_id=self.database_id,
                collection_id=ID.unique(),
                name=class_info['name']
            )
            
            for attr in class_info['attributes']:
                self.create_attribute(collection['$id'], attr)
            
            print(f"Collection '{class_info['name']}' created successfully.")
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to create collection: {str(e)}")
    
    def list_collections(self) -> List[Dict[str, Any]]:
        try:
            collections = self.databases.list_collections(self.database_id)
            return collections['collections']
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to list collections: {str(e)}")
        
    def update_collection(self, collection_id: str, class_info: Dict[str, Any]) -> None:
        #TODO: update method is not working properly. test and fix it
        try:
            # Update collection name if necessary
            self.databases.update_collection(
                database_id=self.database_id,
                collection_id=collection_id,
                name=class_info['name']
            )
            
            existing_attributes = self.databases.list_attributes(self.database_id, collection_id)
            
            for attr in class_info['attributes']:
                existing_attr = next((a for a in existing_attributes['attributes'] if a['key'] == attr['key']), None)
                if existing_attr:
                    self.update_attribute(collection_id, attr, existing_attr)
                else:
                    self.create_attribute(collection_id, attr)
            
            print(f"Collection '{collection_id}' updated successfully.")
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to update collection: {str(e)}")
  
    def create_attribute(self, collection_id: str, attr: Dict[str, Any]) -> None:
        try:
            attr_type = attr['type'].lower()
            method_name = self._get_attribute_method_name(attr_type, 'create')
            create_method = getattr(self.databases, method_name, None)
            
            if not create_method:
                raise ValueError(f"Unsupported attribute type: {attr_type}")
            
            kwargs = self._prepare_attribute_kwargs(attr)
            
            if attr_type == 'relationshipattribute':
                kwargs.update({
                    'related_collection_id': attr.get('related_collection_id'),
                    'type': attr.get('type'),
                    'two_way': attr.get('two_way', False),
                    'two_way_key': attr.get('two_way_key'),
                    'on_delete': attr.get('on_delete')
                })
            elif attr_type == 'enumattribute':
                kwargs['elements'] = attr['elements']
                
                print(kwargs)
            
            create_method(database_id=self.database_id, collection_id=collection_id, **kwargs)
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to create attribute: {str(e)}")

    def update_attribute(self, collection_id: str, updated_attr: Dict[str, Any], old_attr: Dict[str, Any]) -> None:
        try:
            attr_type = updated_attr['type'].lower()
            method_name = self._get_attribute_method_name(attr_type, 'update')
            update_method = getattr(self.databases, method_name, None)
            
            if not update_method:
                raise ValueError(f"Unsupported attribute type: {attr_type}")
            
            kwargs = self._prepare_attribute_kwargs(updated_attr, old_attr)
            
            if attr_type == 'relationshipattribute':
                kwargs['on_delete'] = updated_attr.get('on_delete')
            elif attr_type == 'enumattribute':
                kwargs['elements'] = updated_attr.get('elements', old_attr.get('elements', []))
            
            update_method(database_id=self.database_id, collection_id=collection_id, **kwargs)
        except Exception as e:
            raise AppwriteDatabaseManagerError(f"Failed to update attribute {updated_attr['key']}: {str(e)}")

    def _prepare_attribute_kwargs(self, attr: Dict[str, Any], old_attr: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        kwargs = {
            'key': attr['key'],
            'required': attr.get('required', old_attr.get('required', False) if old_attr else False),
            'default': attr.get('default', old_attr.get('default') if old_attr else None),
        }

        for field in ['size', 'min', 'max', 'array']:
            if field in attr:
                kwargs[field] = attr[field]

        if attr['type'].lower() == 'datetimeattribute' and kwargs['default'] == 'Now':
            kwargs['default'] = datetime.now().isoformat()

        return kwargs

    @staticmethod
    def _get_attribute_method_name(attr_type: str, action: str) -> str:
        attr_type = attr_type.replace('attribute', '')
        if attr_type == 'ipaddress':
            attr_type = 'ip'
        return f"{action}_{attr_type}_attribute"