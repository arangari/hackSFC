import java.util.*;
public class Database {
	public interface Batchable<T>{

	}

	public class BatchableContext{
		public ID getJobId(){
			return new ID();
		}
	}

	public static class querylocator{

	}

	public static querylocator getQueryLocator(String query){
		return new querylocator();
	}

	public static Savepoint setSavepoint(){
		return new Savepoint();
	}

	public static void Rollback(Savepoint sp){

	}

	public static void insert(List<? extends sObject> objects, boolean isInsert){

	}
	public static void update(List<? extends sObject> objects, boolean isInsert){

	}
	public static void delete(List<? extends sObject> objects, boolean isInsert){

	}
	public static void upsert(List<? extends sObject> objects, boolean isInsert){

	}
}
