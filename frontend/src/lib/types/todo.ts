export enum TodoStatusEnum {
  Todo = "todo",
  InProgress = "in_progress",
  Done = "done",
}

export interface createListType{
    title: string
    description: string
    status: TodoStatusEnum

}

export interface updateStatus{
    status: TodoStatusEnum
    id:string

}

export type TodoStatus = (typeof TodoStatusEnum)[keyof typeof TodoStatusEnum];
