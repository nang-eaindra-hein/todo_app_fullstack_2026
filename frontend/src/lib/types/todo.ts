export enum TodoStatusEnum {
  Todo = "Todo",
  InProgress = "In_Progress",
  Done = "Done",
}
export type TodoStatus = (typeof TodoStatusEnum)[keyof typeof TodoStatusEnum];


export interface createListType{
    title: string
    description: string
    status: TodoStatusEnum

}

export interface updateStatusType{
    status: TodoStatusEnum
    id:string

}

export interface updateListType{
    id:number
    title: string
    description: string
    status: TodoStatusEnum
}

export type TodoType = {
	id: number;
	title: string;
	description: string;
	status: TodoStatus
};

export type TodosResponse = {
	items: TodoType[];
	count: { all: number; todo: number; in_progress: number; done: number };
};

