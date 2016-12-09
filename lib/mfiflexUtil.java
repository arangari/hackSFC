import java.util.*;
public class mfiflexUtil {
	
	public static class ExecutionContext{
		public static ExecutionContext getExecContext(){
			return new ExecutionContext();
		}
		
		public ObjectCache getObject(String str){
			return null;
		}
		
		public ObjectCache createObject(String str, String str1){
			return null;
		}
		
	}
	
	public class ObjectCache{
		// getters
	    String getObjectName(){
	    	return null;
	    }
	    String getSObjectName(){
	    	return null;
	    }
	    String getLimitClause(){
	    	return null;
	    }
	    String getWhereClause(){
	    	return null;
	    }
	    String getOrderClause(){
	    	return null;
	    }
	    String lastSuccessfulQuery(){
	    	return null;
	    }
	    
	    Set<String> getFields(){
	    	return null;
	    }
	    List<ObjectCache> getRelationships(){
	    	return null;
	    }
	    
	    // setters
	    ObjectCache setLimitClause(String limitClause){
	    	return null;
	    }
	    ObjectCache setWhereClause(String whereClause){
	    	return null;
	    }
	    ObjectCache setOrderClause(String orderClause){
	    	return null;
	    }  
	    
	    // add fields, relationships and named parameters
	    ObjectCache addFields(String fieldsToBeAdded){
	    	return null;
	    }
	    ObjectCache addFields(List<String> fields){
	    	return null;
	    }  
	    ObjectCache addNamedParameter(String name, Object obj){
	    	return null;
	    }
	    ObjectCache addRelationship(ObjectCache obj){
	    	return null;
	    }
	    
	    // Records related
	    List<? extends sObject> getRecords(){
	    	return null;
	    }
	    
	    Map<ID, sObject> getRecordsMap(){
	    	return null;
	    }
	    void clearRecords(){
	    	
	    }
	    
	    // Query related
	    String getQuery(){
	    	return null;
	    }
	    ObjectCache buildQuery(){
	    	return null;
	    }
	    ObjectCache executeQuery(){
	    	return null;
	    }
	}
}
