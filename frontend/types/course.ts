export interface Unit {
  id: string;
  course_id: string;
  title: string;
  description: string | null;
  order_index: number;
}

export interface CourseSummary {
  id: string;
  name: string;
  code: string;
  source_language: string;
  target_language: string;
  description: string | null;
  is_active: boolean;
}

export interface CourseDetail extends CourseSummary {
  units: Unit[];
}
